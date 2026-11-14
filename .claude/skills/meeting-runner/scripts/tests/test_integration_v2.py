"""Integração dos scripts com o `brza sessions` v2 REAL (o arquivo do brza-workflow), sem produção.

O `brza-sessions` é carregado por `SourceFileLoader`; o app e o `brza orchestration` são trocados por um fake que devolve
os FORMATOS REAIS das fixtures da sonda (recibo do `worker-start` do P7, `worker-show`, mensagens do mailbox e do `wait`).
O corredor do `launch_persona`/`wait_round` chama `main()` do v2 em processo. Nenhum comando real do brza roda, e nada
toca o Studio.
"""
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import _paths  # noqa: F401
from _paths import fixture, le

import launch_persona
import tally
import wait_round

try:
    import sessions_map
except ImportError:  # snapshot anterior ao v2
    sessions_map = None

BRZA_SESSIONS = Path(os.path.expanduser("~/Projects/brza-workflow/packages/client/bin/brza-sessions"))
os.environ["BRZA_REGISTRY"] = "/nonexistent/brza/workspaces.toml"  # nada aqui lê o registro real da máquina

UUID_CLAUDE = "cd289115-4fab-49e4-bc30-58247c2cfe74"
PROV_GROK = "grok-prov-0001"
CHAT_CLAUDE = "4c71586a-b184-4633-81e6-2e3e1e31fe1a"   # o `endpointIncarnation` do worker-show real do Claude
CHAT_GROK = "39bfff09-2d0c-4977-9a3e-14bcbeeb15bb"     # o do Grok


def carrega_v2():
    """Carrega o brza-sessions real; `skipTest` só se o arquivo não existir (nunca por exceção)."""
    if not BRZA_SESSIONS.is_file():
        raise unittest.SkipTest(f"o brza-sessions real não existe em {BRZA_SESSIONS}: sem o brza-workflow ao lado, "
                                "a integração com o v2 não roda")
    loader = importlib.machinery.SourceFileLoader("brza_sessions_real", str(BRZA_SESSIONS))
    spec = importlib.util.spec_from_loader("brza_sessions_real", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def recibo_real(slug):
    """O `result` do `worker-start --json` do P7, tal como gravado em `launch-<slug>.log`."""
    texto = le("p7", f"launch-{slug}.log")
    linha = texto.split("--- stdout\n", 1)[1].split("\n", 1)[0]
    return json.loads(linha)["result"]


def show_real(nome):
    d = json.loads(le("v2", nome))
    return copy.deepcopy(d["result"] if isinstance(d.get("result"), dict) else d)


class FakeTime:
    """O `time` do v2: o relógio anda só quando o código dorme, e a espera inteira é instantânea."""

    def __init__(self):
        self.agora = 0.0

    def monotonic(self):
        return self.agora

    def sleep(self, s):
        self.agora += s

    def time(self):
        import time as real
        return real.time() + self.agora


class FakeApp:
    """O app e o `brza orchestration`, com os formatos reais; guarda cada chamada para o teste conferir."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.calls = []           # [(args do brza)]
        self.enviados = []        # [(chat, texto, operation)]
        self.tabs = []
        self.mensagens = []       # o mailbox do Run
        self.provider_chamadas = {}
        self.mostra = {}          # dispatch -> o `result` do worker-show
        self.recibos = {"ci-prumo": recibo_real("prumo"), "ci-trava": recibo_real("trava")}
        self.stop_modo = "stop_unknown"
        self.send_status = {CHAT_CLAUDE: "accepted", CHAT_GROK: "pending"}

    # -- o `brza orchestration …` (devolve o `result`, como o `brza()` do runtime)
    def brza(self, *args):
        self.calls.append(args)
        if args[:2] == ("orchestration", "worker-start"):
            nome = "ci-prumo" if "claude" in args else "ci-trava"
            r = copy.deepcopy(self.recibos[nome])
            chat = CHAT_CLAUDE if nome == "ci-prumo" else CHAT_GROK
            base = show_real("pure-grok-show.json")      # ready/input_accepted: o worker ativo
            base["dispatch"]["id"] = r["dispatchId"]
            base["dispatch"]["runId"] = r["runId"]
            base["terminalResource"]["endpointIncarnation"] = "structured:" + chat
            self.mostra[r["dispatchId"]] = base
            self.tabs.append({"type": "agent-session", "id": "agent-session:" + chat, "sessionId": chat,
                              "title": nome, "chatStatus": {"state": "working"}, "agent": "claude" if chat == CHAT_CLAUDE else "grok"})
            return r
        if args[:2] == ("orchestration", "worker-show"):
            return copy.deepcopy(self.mostra[args[args.index("--dispatch") + 1]])
        if args[:2] == ("orchestration", "check"):
            return {"messages": copy.deepcopy(self.mensagens)}
        if args[:2] == ("orchestration", "send"):
            return {"messageId": "msg_b4c0cdbb92a2"}                # o recibo real do `closing`
        if args[:2] == ("orchestration", "worker-stop"):
            from_runtime = sys.modules["brza_runtime"].BrzaError
            raise from_runtime("worker-stop: resultado incerto", body={"error": {"code": self.stop_modo}})
        if args[:2] == ("orchestration", "worker-release"):
            return {"state": "released"}
        raise AssertionError(f"chamada inesperada ao brza: {args}")

    # -- o app
    def rpc(self, method, params=None):
        if method == "agentSession.rename":
            return {"ok": True}
        if method == "agentSession.history":
            return {"page": {"fence": 3}}
        raise AssertionError(f"rpc inesperado: {method}")

    def open_tabs(self):
        return [("wt", t) for t in self.tabs]

    def provider_session(self, chat):
        n = self.provider_chamadas[chat] = self.provider_chamadas.get(chat, 0) + 1
        if n == 1:
            return None            # o app ainda não deu o id quando o worker abre: o `open` sai sem ele
        return UUID_CLAUDE if chat == CHAT_CLAUDE else PROV_GROK

    def send_to_chat(self, chat, texto, operation=None):
        self.enviados.append((chat, texto, operation))
        return {"ok": True, "replayed": False, "value": {"submission": {"dispatchState": self.send_status[chat]}}}

    # -- o mailbox
    def status(self, sessao_sender, dispatch, round_id, id=None):
        self.mensagens.append({"id": id or f"msg_{len(self.mensagens)}", "type": "status", "from": sessao_sender,
                               "subject": "brza-sessions-round", "payload": {"round_id": round_id, "dispatchId": dispatch}})


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v2 = carrega_v2()

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.ws = self.tmp
        (self.ws / ".sessions").mkdir()
        (self.ws / ".measurements").mkdir()
        self.mapa = self.ws / ".sessions" / "sessions.jsonl"
        self.app = FakeApp(self.tmp)
        self.tempo = FakeTime()
        trocas = {"WORKSPACE": self.ws, "SESSION_MAP": self.mapa, "brza": self.app.brza, "rpc": self.app.rpc,
                  "send_to_chat": self.app.send_to_chat, "provider_session": self.app.provider_session,
                  "coordinator_identity": lambda: "orca_session_id:coordenacao", "open_tabs": self.app.open_tabs,
                  "running": lambda nome: False, "config_dirs": lambda: [self.tmp / "config"], "time": self.tempo}
        for nome, valor in trocas.items():
            original = getattr(self.v2, nome)
            setattr(self.v2, nome, valor)
            self.addCleanup(setattr, self.v2, nome, original)
        self.reuniao = self.escreve_reuniao()
        self.manifesto = str(self.ws / "reuniao.json")

    def escreve_reuniao(self):
        p7 = json.loads(le("p7", "reuniao.json"))
        reuniao = {k: p7[k] for k in ("id", "tema", "decisor", "fim", "data", "checkout", "dir", "worklog", "briefing")}
        reuniao["personas"] = [{k: v for k, v in p.items() if k not in ("dispatch_id", "claude_session", "provider_session")}
                               for p in p7["personas"][:2]]            # Prumo (claude) e Trava (grok)
        os.makedirs(self.ws / reuniao["dir"], exist_ok=True)
        (self.ws / ".worktrees" / "playground").mkdir(parents=True)
        with open(self.ws / "reuniao.json", "w", encoding="utf-8") as f:
            json.dump(reuniao, f, ensure_ascii=False)
        for n in (2,):
            with open(self.ws / reuniao["dir"] / f"rodada-{n}.md", "w", encoding="utf-8") as f:
                f.write(f"# Rodada {n} — debate (duração: ~2 min)\n")
        return reuniao

    # -- os corredores do launch_persona e do wait_round, em processo
    def v2_main(self, argv):
        saida, erro = io.StringIO(), io.StringIO()
        antes = sys.argv
        sys.argv = ["brza-sessions", *argv]
        try:
            with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(erro):
                rc = self.v2.main()
        finally:
            sys.argv = antes
        return rc, saida.getvalue(), erro.getvalue()

    def lancar(self, *args, **kw):
        out = []
        rc = launch_persona.main([self.manifesto, *args, "--root", str(self.ws), "--sessions", str(self.mapa)],
                                 sessions_fn=self.v2_main, brza_fn=lambda argv: (0, json.dumps({"ok": True, "result": self.app.brza(*argv)}), ""),
                                 out=out.append, **kw)
        return rc, "\n".join(out)

    def esperar(self, *args):
        """`wait_round.main` com o `brza sessions wait` em processo."""
        original = wait_round.wait_brza

        def wait_fn(sessoes, timeout_s):
            rc, so, se = self.v2_main(wait_round.wait_argv(sessoes, timeout_s))
            return rc, json.loads(so)
        wait_round.wait_brza = wait_fn
        relogio, wait_round.time = wait_round.time, self.tempo     # o mesmo relógio falso do v2: sem laço quente
        saida = io.StringIO()
        try:
            with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(io.StringIO()):
                rc = wait_round.main(["2", "--reuniao", self.manifesto, "--root", str(self.ws), "--sessions", str(self.mapa),
                                      "--no-state", "--no-panel", *args])
        finally:
            wait_round.wait_brza, wait_round.time = original, relogio
        return rc, saida.getvalue()

    def linhas_do_mapa(self):
        return [json.loads(l) for l in self.mapa.read_text().splitlines()]

    def abre(self):
        rc, s = self.lancar()
        self.assertEqual(rc, 0, s)
        return s


class Abertura(Base):
    def test_abre_uma_a_uma_e_grava_a_identidade_inteira_no_mapa(self):
        s = self.abre()
        entradas = sessions_map.load_map(str(self.ws), str(self.mapa))
        prumo, trava = entradas["ci-prumo"], entradas["ci-trava"]
        self.assertEqual(prumo["dispatch"], "ctx_80fad49a44fd")
        self.assertEqual(trava["dispatch"], "ctx_f7391bdf18a4")
        self.assertEqual(prumo["run"], trava["run"])                          # UM Run só
        self.assertEqual(prumo["run"], "run_fe70b351bc36")
        self.assertEqual(prumo["sender"], "structworker_271da48e-9b93-4ac7-a4d3-6af0dda6e5e0")
        self.assertEqual(prumo["coordinator"], "orca_session_id:coordenacao")
        # o id do provedor chegou depois do `--wait` (identidade persistida, X1): `open` sem id e `session` depois
        abre = [l for l in self.linhas_do_mapa() if l["event"] == "open" and l["name"] == "ci-prumo"][0]
        self.assertIsNone(abre["claude_session"])
        self.assertEqual((prumo["claude_session"], prumo["provider_session"]), (UUID_CLAUDE, UUID_CLAUDE))
        self.assertEqual(trava["provider_session"], PROV_GROK)
        self.assertIsNone(trava["claude_session"])
        # a ordem das aberturas e o modelo/esforço do manifesto chegam ao worker-start
        starts = [a for a in self.app.calls if a[:2] == ("orchestration", "worker-start")]
        self.assertEqual([a[a.index("--agent") + 1] for a in starts], ["claude", "grok"])
        self.assertEqual(starts[0][starts[0].index("--model") + 1], "claude-opus-5-5")
        self.assertEqual(starts[0][starts[0].index("--effort") + 1], "xhigh")
        self.assertEqual(starts[1][starts[1].index("--model") + 1], "grok-4.7")
        self.assertIn("Protocolo da persona", starts[0][starts[0].index("--spec") + 1])   # o v2 anexa o protocolo
        # a tabela da narração
        self.assertIn("Prumo · Cético medidor · claude · claude-opus-5-5 · xhigh · ctx_80fad49a44fd · run_fe70b351bc36 · "
                      + UUID_CLAUDE, s)
        self.assertIn("Trava · Guardião de contenção · grok · grok-4.7 · medium · ctx_f7391bdf18a4 · run_fe70b351bc36 · "
                      + PROV_GROK, s)
        self.assertNotIn("Run múltiplo", s)

    def test_o_prompt_gerado_nao_tem_comando_de_orchestration_proprio(self):
        self.abre()
        spec = next(a for a in self.app.calls if a[:2] == ("orchestration", "worker-start"))[
            next(a for a in self.app.calls if a[:2] == ("orchestration", "worker-start")).index("--spec") + 1]
        self.assertNotIn("brza orchestration send", spec.split("Protocolo da persona")[0])
        self.assertIn("--task-id", spec)

    def test_abrir_de_novo_nao_reabre(self):
        self.abre()
        n = len([a for a in self.app.calls if a[:2] == ("orchestration", "worker-start")])
        rc, s = self.lancar()
        self.assertEqual(rc, 0)
        self.assertIn("já aberta; não reabre", s)
        self.assertEqual(len([a for a in self.app.calls if a[:2] == ("orchestration", "worker-start")]), n)


class Rodada(Base):
    def setUp(self):
        super().setUp()
        self.abre()
        self.e = sessions_map.load_map(str(self.ws), str(self.mapa))

    def envia(self):
        return self.lancar("--send", "--round", "2")

    def test_send_registra_round_id_igual_a_operation_e_o_texto_leva_o_protocolo_com_o_dispatch(self):
        rc, s = self.envia()
        sends = [l for l in self.linhas_do_mapa() if l["event"] == "send"]
        self.assertEqual(len(sends), 2)
        for l in sends:
            self.assertEqual(l["round_id"], l["operation"])
        texto = next(t for c, t, o in self.app.enviados if c == CHAT_CLAUDE)
        self.assertTrue(texto.startswith(f"Faça a rodada 2: {self.reuniao['dir']}/rodada-2.md"))
        self.assertIn("--type status --subject brza-sessions-round", texto)
        op = next(o for c, t, o in self.app.enviados if c == CHAT_CLAUDE)
        self.assertIn(json.dumps({"round_id": op, "dispatchId": "ctx_80fad49a44fd"}, ensure_ascii=False), texto)
        # Claude aceitou; o Grok ficou `pending`: rc 75 e a instrução literal, sem reenviar
        self.assertEqual(rc, 75)
        self.assertIn("Trava: pending — não reenvie às cegas; espere com wait_round.py 2, ou repita só esta persona com "
                      "--operation", s)
        self.assertIn("Prumo: accepted", s)
        self.assertEqual(len(self.app.enviados), 2)

    def test_status_certo_conclui_a_rodada_e_o_errado_nao(self):
        self.envia()
        prumo, trava = self.e["ci-prumo"], self.e["ci-trava"]
        op_p = next(o for c, t, o in self.app.enviados if c == CHAT_CLAUDE)
        op_t = next(o for c, t, o in self.app.enviados if c == CHAT_GROK)
        # round_id velho (o do open), remetente de outro worker e o ruído do fim de turno: NÃO concluem
        self.app.status(prumo["sender"], prumo["dispatch"], prumo_op_velho(self.e), id="velho")
        self.app.status(trava["sender"], prumo["dispatch"], op_p, id="outro-remetente")
        self.app.mensagens.append({"id": "ruido", "type": "escalation", "from": prumo["sender"],
                                   "subject": "Worker stopped without reporting",
                                   "payload": {"taskId": "task_x", "dispatchId": prumo["dispatch"], "stopReason": "finished"}})
        rc, s = self.esperar("--timeout", "10")
        self.assertEqual(rc, 2, s)
        self.assertIn("R2 · 0/2 — faltam Prumo (Claude) e Trava (Grok)", s)
        self.assertIn('ruído previsto: 1 avisos "Worker stopped without reporting"', s)
        self.assertNotIn("entregaram", s)
        # o status certo do Prumo conclui só o Prumo; o do Grok conclui o resto
        self.app.status(prumo["sender"], prumo["dispatch"], op_p, id="certo-p")
        self.escreve_worklog("prumo", 2)
        rc, s = self.esperar("--timeout", "10")
        self.assertEqual(rc, 2, s)
        self.assertIn("R2 · 1/2 — entregaram Prumo; faltam Trava (Grok", s)
        self.app.status(trava["sender"], trava["dispatch"], op_t, id="certo-t")
        self.escreve_worklog("trava", 2)
        rc, s = self.esperar("--timeout", "10")
        self.assertEqual(rc, 0, s)
        self.assertIn("todos entregaram", s)
        turnos = [l for l in self.linhas_do_mapa() if l["event"] == "turn"]
        self.assertEqual({t["name"] for t in turnos}, {"ci-prumo", "ci-trava"})

    def escreve_worklog(self, slug, n):
        path = self.ws / "work" / "worklogs" / f"2026-11-09-reuniao-ci-no-chat-{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {slug}\n\n### Rodada {n}: debate\n\n- **Posição:** A.\n\n"
                        f"| Parte | Anterior | Atual | Porquê |\n| :-- | :-- | :-- | :-- |\n| **O plano inteiro** | 70 | 80 | x |\n\n"
                        f"<!-- fim-rodada-{n} -->\n", encoding="utf-8")

    def test_sem_send_registrado_o_erro_do_v2_aparece_e_nao_cai_para_o_marcador(self):
        # apaga o `send` e o round do open para esta sessão: o v2 diz "nenhum send registrado"
        linhas = [l for l in self.linhas_do_mapa()]
        for l in linhas:
            if l["event"] == "open":
                l.pop("operation", None)
                l.pop("round_id", None)
        self.mapa.write_text("".join(json.dumps(l) + "\n" for l in linhas))
        self.escreve_worklog("prumo", 2)
        self.escreve_worklog("trava", 2)
        rc, s = self.esperar("--timeout", "10")
        self.assertEqual(rc, 1)
        self.assertIn("erro do brza sessions wait: ci-prumo: nenhum send registrado para esperar", s)
        self.assertNotIn("entregaram", s)


def prumo_op_velho(entradas):
    return entradas["ci-prumo"]["last_send"]["round_id"]     # o round_id do `open` (a rodada 1)


class Encerramento(Base):
    def setUp(self):
        super().setUp()
        self.abre()
        self.d_prumo, self.d_trava = "ctx_80fad49a44fd", "ctx_f7391bdf18a4"

    def test_close_devolve_closing_e_o_script_nao_diz_fechada(self):
        rc, s = self.lancar("Prumo", "--close")
        self.assertEqual(rc, 0, s)
        self.assertIn("pedido de encerramento enviado; NÃO está fechada; confira com --status", s)
        self.assertNotIn("fechada (", s)
        self.assertFalse([l for l in self.linhas_do_mapa() if l["event"] == "close"])   # o v2 não grava close em `closing`

    def test_status_com_o_worker_show_succeeded_settled_diz_encerrada_e_aceita(self):
        self.app.mostra[self.d_prumo] = {**show_real("pure-claude-show.json")}
        self.app.mostra[self.d_prumo]["dispatch"]["id"] = self.d_prumo
        rc, s = self.lancar("Prumo", "--status")
        self.assertEqual(rc, 0, s)
        self.assertIn("task_f82ca8f37528", s)
        self.assertIn("→ encerrada e aceita", s)

    def test_stop_unknown_sai_75_sem_repetir_a_chamada(self):
        rc, s = self.lancar("Trava", "--stop")
        self.assertEqual(rc, 75, s)
        self.assertIn("incerto (stop_unknown): não está fechada; não repita; confira com --status", s)
        paradas = [a for a in self.app.calls if a[:2] == ("orchestration", "worker-stop")]
        self.assertEqual(len(paradas), 1)
        self.assertEqual(len([a for a in self.app.calls if a[:2] == ("orchestration", "worker-release")]), 0)

    def test_released_fecha_e_a_medicao_acha_a_persona_depois_do_auto_release(self):
        # o worker terminou (succeeded/settled); o close libera e o v2 grava `close` no mapa
        # ACHADO (v2, fora desta tarefa): o `worker_state` do brza-sessions lê `dispatch.status` ANTES de `worker.state`; no
        # formato real o primeiro é "completed", que não está em ('succeeded', ...), e o `close` de um worker já encerrado
        # volta `closing`. Aqui o campo sai do worker-show para exercitar o `released`.
        liberavel = show_real("pure-claude-show.json")      # succeeded/settled, ainda `not_requested`
        liberavel["dispatch"]["id"] = self.d_prumo
        del liberavel["dispatch"]["status"]
        self.app.mostra[self.d_prumo] = liberavel
        rc, s = self.lancar("Prumo", "--close")
        self.assertEqual(rc, 0, s)
        self.assertIn("fechada (released)", s)
        self.assertEqual([l["name"] for l in self.linhas_do_mapa() if l["event"] == "close"], ["ci-prumo"])
        # o hook mediu o turno do Claude; o tally o acha pelo id do MAPA, mesmo com a sessão fechada
        wl = self.ws / "work" / "worklogs"
        wl.mkdir(parents=True)
        for slug in ("prumo", "trava"):
            (wl / f"2026-11-09-reuniao-ci-no-chat-{slug}.md").write_text(
                "### Rodada 2: debate\n\n- **Posição:** A.\n\n<!-- fim-rodada-2 -->\n", encoding="utf-8")
        with open(self.ws / ".measurements" / "measurements.jsonl", "w", encoding="utf-8") as f:
            f.write(json.dumps({"event": "turn", "session_id": UUID_CLAUDE, "timestamp": "2026-11-09T21:38:00+00:00",
                                "estimated_cost_usd": 1.75, "duration_s": 55}) + "\n")
        estado = tally.build_estado(self.reuniao, 2, str(self.ws), measurements=str(self.ws / ".measurements/measurements.jsonl"),
                                    sessions=str(self.mapa), codex_dir=str(self.tmp / "x"))
        prumo = next(p for p in estado["personas"] if p["nome"] == "Prumo")
        self.assertEqual((prumo["custo_usd"], prumo["medicao"]), (1.75, "medida"))


class ContratoComOArgparseReal(Base):
    """Cada linha `brza sessions …` que os scripts montam passa no argparse REAL do v2, sem executar o verbo."""

    def setUp(self):
        super().setUp()
        self.verbos = []
        for verbo in ("send_command", "close_command", "wait_command"):
            original = getattr(self.v2, verbo)

            def falso(args, _v=verbo):
                self.verbos.append((_v, args))
                return 0
            setattr(self.v2, verbo, falso)
            self.addCleanup(setattr, self.v2, verbo, original)

    def passa(self, argv):
        antes = len(self.verbos)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            rc = self.v2.by_name(argv)
        self.assertEqual(rc, 0, (argv, err.getvalue()))
        self.assertEqual(len(self.verbos), antes + 1, argv)
        return self.verbos[-1]

    def test_send(self):
        _, a = self.passa(launch_persona.send_argv(["ci-prumo", "ci-trava"], "Faça a rodada 2: x", None))
        self.assertEqual((a.names, a.text, a.json, a.operation), (["ci-prumo", "ci-trava"], "Faça a rodada 2: x", True, None))
        _, a = self.passa(launch_persona.send_argv(["ci-trava"], "mesmo texto", "op-123"))
        self.assertEqual((a.names, a.operation), (["ci-trava"], "op-123"))

    def test_close_nos_tres_modos(self):
        for modo, force, keep in (("close", False, False), ("stop", True, False), ("keep-open", False, True)):
            _, a = self.passa(launch_persona.close_argv("ci-prumo", modo))
            self.assertEqual((a.name, a.force, a.keep_open, a.json), ("ci-prumo", force, keep, True), modo)

    def test_wait(self):
        _, a = self.passa(wait_round.wait_argv(["ci-prumo", "ci-trava"], 180))
        self.assertEqual((a.names, a.any, a.timeout, a.json), (["ci-prumo", "ci-trava"], True, 180.0, True))
        _, a = self.passa(wait_round.wait_argv(["ci-prumo"], 0))
        self.assertEqual(a.timeout, 0.0)

    def test_open_de_cada_persona_do_manifesto_passa_no_parser_do_v2(self):
        """O `open` não tem verbo: o `--dry-run` faz o v2 ler todos os flags e sair antes de abrir."""
        for p in self.reuniao["personas"]:
            launch_persona.ensure_prompt(self.reuniao, p, str(self.ws))
            argv = launch_persona.open_argv(self.reuniao, p, str(self.ws))
            self.assertTrue(Path(argv[argv.index("--checkout") + 1]).is_absolute())
            rc, out, err = self.v2_main(argv + ["--dry-run"])
            self.assertEqual(rc, 0, (argv, out, err))
            self.assertIn(f"abriria:  {p['sessao']}", out)
        self.assertEqual(self.app.calls, [])    # nada foi aberto

    def test_os_flags_antigos_nao_passam_no_v2(self):
        """A prova de que a lista antiga estava errada: `--to`/`--subject` não existem no `brza sessions send`."""
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.v2.by_name(["send", "ci-prumo", "--subject", "rodada", "--body", "x"])


if __name__ == "__main__":
    unittest.main()
