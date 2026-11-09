"""Testes do launch_persona.py: só com --dry-run (nenhuma sessão é aberta e nenhum prompt é gravado)."""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import launch_persona  # noqa: E402

with open(os.path.join(HERE, "fixtures", "reuniao-mcp-remoto.json"), encoding="utf-8") as _f:
    REUNIAO = json.load(_f)


def _le(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class DryRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.manifesto = os.path.join(self.tmp, "reuniao.json")
        with open(self.manifesto, "w", encoding="utf-8") as f:
            json.dump(REUNIAO, f, ensure_ascii=False)
        os.makedirs(os.path.join(self.tmp, REUNIAO["dir"]))

    def roda(self, *args, via="agent-launch"):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = launch_persona.main([self.manifesto, *args, "--via", via, "--dry-run", "--root", self.tmp])
        self.assertEqual(rc, 0)
        return buf.getvalue()

    def bloco(self, saida, nome):
        partes = saida.split("[dry-run] ")
        return next(p for p in partes if p.startswith(nome + " "))

    def test_todas_as_personas_com_modelo_e_esforco(self):
        saida = self.roda()
        self.assertEqual(saida.count("[dry-run] "), 6)
        m = self.bloco(saida, "Muralha")
        self.assertIn("brza agent launch --agent claude --surface chat --worktree path:<checkout> [--prompt ...] "
                      "--model opus-5.5 --effort high", m)
        self.assertIn("mapa: open model=opus-5.5 effort=high", m)
        self.assertIn("--checkout .worktrees/playground", m)
        self.assertIn("mcp-muralha --agent claude", m)
        self.assertIn("--wait", m)
        self.assertIn(os.path.join(self.tmp, ".sessions/reuniao-mcp-remoto/prompt-muralha.txt"), m)

    def test_codex_e_grok_repassam(self):
        saida = self.roda()
        self.assertIn("--model gpt-6-astra --effort xhigh", self.bloco(saida, "Régua"))
        self.assertIn("--model grok-4.7-build-fast --effort low", self.bloco(saida, "Salto"))

    def test_antigravity_nunca_leva_modelo(self):
        c = self.bloco(self.roda("Cartógrafo"), "Cartógrafo")
        self.assertNotIn("--model", c)
        self.assertNotIn("--effort", c)
        self.assertIn("mapa: open model=- effort=-", c)
        # mesmo que o manifesto traga um modelo para o Antigravity, o chat o recusaria
        REUNIAO["personas"][5]["modelo"] = "gemini-4-argon"
        try:
            with open(self.manifesto, "w", encoding="utf-8") as f:
                json.dump(REUNIAO, f, ensure_ascii=False)
            self.assertNotIn("--model", self.bloco(self.roda("cartografo"), "Cartógrafo"))
        finally:
            REUNIAO["personas"][5]["modelo"] = "-"

    def test_modelo_nulo_ou_traco_nao_vira_flag(self):
        p = {"nome": "X", "slug": "x", "sessao": "s-x", "runtime": "claude", "modelo": None, "esforco": "high"}
        self.assertEqual(launch_persona.agent_launch_extra(p), [])
        p["modelo"] = "-"
        self.assertEqual(launch_persona.agent_launch_extra(p), [])
        p["modelo"], p["esforco"] = "m", "-"
        self.assertEqual(launch_persona.agent_launch_extra(p), ["--model", "m"])

    def test_escolha_por_nome_slug_ou_sessao(self):
        saida = self.roda("plantao", "mcp-salto", "Régua")
        self.assertEqual(saida.count("[dry-run] "), 3)
        with self.assertRaises(SystemExit):
            self.roda("ninguem")

    def test_prompt_gerado_nao_e_gravado_no_dry_run(self):
        saida = self.roda("Salto")
        self.assertIn("geraria", saida)
        self.assertIn("MCP remoto e sessões Cloud", saida)
        self.assertIn("work/worklogs/2026-11-07-reuniao-mcp-remoto-salto.md", saida)
        self.assertIn("22h15", saida)
        self.assertIn("Você é uma persona", saida)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, ".sessions/reuniao-mcp-remoto/prompt-salto.txt")))

    def test_prompt_existente_e_respeitado(self):
        with open(os.path.join(self.tmp, ".sessions/reuniao-mcp-remoto/prompt-salto.txt"), "w") as f:
            f.write("meu prompt\n")
        self.assertIn("(existe)", self.roda("Salto"))

    def test_worker_start_e_o_padrao(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            launch_persona.main([self.manifesto, "Muralha", "--dry-run", "--root", self.tmp])
        m = buf.getvalue()
        self.assertIn("via worker-start", m)
        self.assertNotIn("'brza sessions'", m)
        self.assertIn("aviso: a linha `open` não terá chat/claude_session/provider_session", m)
        self.assertIn("brza orchestration worker-start --spec-file " + os.path.join(
            self.tmp, ".sessions/reuniao-mcp-remoto/prompt-muralha.txt") + " --agent claude --model opus-5.5 "
            "--effort high --worktree path:" + os.path.join(self.tmp, ".worktrees/playground") + " --json", m)
        self.assertIn("launch-muralha.log", m)
        self.assertIn("mapa: open model=opus-5.5 effort=high via=worker-start dispatch_id=", m)

    def test_worker_start_antigravity_sem_modelo(self):
        c = self.roda("Cartógrafo", via="worker-start")
        self.assertIn("--agent antigravity", c)
        self.assertNotIn("--model", c)
        self.assertNotIn("--effort", c)

    def test_hybrid_abre_o_chat_e_depois_o_worker_start_no_terminal(self):
        m = self.roda("Muralha", via="hybrid")
        self.assertIn("'brza sessions' mcp-muralha --agent claude", m)
        self.assertIn("brza agent launch --agent claude --surface chat", m)
        self.assertIn("worker-start --spec-file", m)
        self.assertIn("--terminal 'orca_session_id:<chat>'", m)
        # C13: reusar o terminal pede o --worktree dele
        self.assertIn("--worktree path:" + os.path.join(self.tmp, ".worktrees/playground"), m[m.index("--terminal"):])
        self.assertLess(m.index("brza sessions"), m.index("--terminal"))

    def test_release_e_keep_open_em_dry_run(self):
        mapa = os.path.join(self.tmp, "mapa.jsonl")
        with open(mapa, "w", encoding="utf-8") as f:
            f.write(json.dumps({"event": "open", "name": "mcp-muralha", "dispatch_id": "velho"}) + "\n")
            f.write(json.dumps({"event": "open", "name": "mcp-muralha", "dispatch_id": "d-9"}) + "\n")
        for flag, verbo in (("--release", "worker-release"), ("--keep-open", "worker-keep-open")):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = launch_persona.main([self.manifesto, flag, "Muralha", "--dry-run", "--root", self.tmp,
                                          "--sessions", mapa])
            self.assertEqual(rc, 0)
            self.assertIn(f"[dry-run] Muralha: brza orchestration {verbo} --dispatch d-9", buf.getvalue())
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(io.StringIO()):
            rc = launch_persona.main([self.manifesto, "--release", "Régua", "--dry-run", "--root", self.tmp,
                                      "--sessions", mapa])
        self.assertEqual(rc, 1)  # sem dispatch no mapa
        self.assertEqual(buf.getvalue(), "")


class Molde(unittest.TestCase):
    def test_os_dois_comandos_sem_coordenacao(self):
        t = launch_persona.prompt_text(REUNIAO, REUNIAO["personas"][0])
        n = REUNIAO["personas"][0]["nome"]
        self.assertIn('brza orchestration send --subject "fim-rodada-N" --body "persona:muralha"', t)
        self.assertIn('brza orchestration send --type worker_done --outcome succeeded --subject "encerrado" '
                      '--body "persona:muralha"', t)
        self.assertNotIn(f'--body "{n}"', t)
        self.assertIn("ENCERRAMENTO", t)
        self.assertNotIn("--to", t)

    def test_coordenacao_do_manifesto_vira_to(self):
        r = dict(REUNIAO, coordenacao="run:abc")
        t = launch_persona.prompt_text(r, r["personas"][0])
        self.assertIn('brza orchestration send --to run:abc --subject "fim-rodada-N"', t)
        self.assertIn('send --to run:abc --type worker_done', t)
        self.assertIn('--subject "encerrado" --body "persona:muralha"', t)


class SendEStop(unittest.TestCase):
    """`--send`, `--stop` e a raiz padrão; nenhum comando do brza roda de verdade (dry-run e run_fn falso)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.manifesto = os.path.join(self.tmp, "reuniao.json")
        with open(self.manifesto, "w", encoding="utf-8") as f:
            json.dump(REUNIAO, f, ensure_ascii=False)
        self.mapa = os.path.join(self.tmp, "mapa.jsonl")
        with open(self.mapa, "w", encoding="utf-8") as f:
            for nome, d in (("mcp-muralha", "d-1"), ("mcp-regua", "d-2")):
                f.write(json.dumps({"event": "open", "name": nome, "dispatch_id": d}) + "\n")

    def main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = launch_persona.main([self.manifesto, *args, "--root", self.tmp, "--sessions", self.mapa])
        return rc, out.getvalue(), err.getvalue()

    def test_send_dry_run_monta_o_comando_sem_shell(self):
        rc, out, _ = self.main("--send", "Muralha", "Régua", "--message", "Faça a rodada 2; use 'aspas' e $VAR", "--dry-run")
        self.assertEqual(rc, 0)
        self.assertIn("[dry-run] Muralha: brza orchestration send --to dispatch:d-1 --subject rodada --body "
                      "'Faça a rodada 2; use '\"'\"'aspas'\"'\"' e $VAR'", out)
        self.assertIn("--to dispatch:d-2", out)
        self.assertEqual(launch_persona.send_argv("d-1", "t"),
                         ["brza", "orchestration", "send", "--to", "dispatch:d-1", "--subject", "rodada", "--body", "t"])

    def test_send_todas_e_sem_dispatch_e_sem_mensagem(self):
        rc, out, err = self.main("--send", "todas", "--message", "x", "--dry-run")
        self.assertEqual(rc, 1)  # as outras quatro personas não têm dispatch no mapa
        self.assertEqual(out.count("[dry-run]"), 2)
        self.assertEqual(err.count("sem dispatch_id"), 4)
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            self.main("--send", "Muralha")

    def test_send_roda_pelo_run_fn_e_o_dispatch_do_manifesto_vale(self):
        chamadas = []
        p = dict(REUNIAO["personas"][0], dispatch_id="man-7")
        with redirect_stdout(io.StringIO()):
            rc = launch_persona.send(REUNIAO, [p], self.tmp, "oi", self.mapa,
                                     run_fn=lambda argv: chamadas.append(argv) or (0, "ok", ""))
        self.assertEqual((rc, chamadas[0][4]), (0, "dispatch:man-7"))

    def test_stop_usa_worker_stop_e_release_continua_so_release(self):
        rc, out, _ = self.main("--stop", "Muralha", "--dry-run")
        self.assertEqual(rc, 0)
        self.assertIn("[dry-run] Muralha: brza orchestration worker-stop --dispatch d-1", out)
        rc, out, _ = self.main("--release", "Muralha", "--dry-run")
        self.assertIn("worker-release --dispatch d-1", out)
        self.assertNotIn("worker-stop", out)

    def test_raiz_padrao_e_o_mesmo_de_qualquer_diretorio(self):
        """C8: sem --root, o topo do git do cwd; do worktree e da pasta da skill dá o mesmo."""
        aqui = os.path.dirname(os.path.dirname(HERE))
        raiz = launch_persona.raiz_padrao()
        antes = os.getcwd()
        try:
            for d in (raiz, aqui, HERE):
                os.chdir(d)
                self.assertEqual(os.path.realpath(launch_persona.raiz_padrao()), os.path.realpath(raiz))
        finally:
            os.chdir(antes)


class Recibo(unittest.TestCase):
    def test_tres_formatos_plausiveis(self):
        f = launch_persona.extract_receipt
        self.assertEqual(f('{"dispatch_id": "d1", "orca_session_id": "claude_a"}'), ("d1", "claude_a"))
        self.assertEqual(f('{"result": {"dispatch": {"id": "d2"}, "terminal": {"x": 1}, "handle": "term_9"}}'),
                         ("d2", "term_9"))
        self.assertEqual(f(json.dumps({"ok": True, "data": [{"dispatchId": "d3", "agentSessionId": "s3",
                                                             "sessionId": "outro"}]})), ("d3", "s3"))

    def test_texto_puro_e_ausencia(self):
        self.assertEqual(launch_persona.extract_receipt("dispatch_id: d4\norca_session_id=s4"), ("d4", "s4"))
        self.assertEqual(launch_persona.extract_receipt('{"nada": 1}'), (None, None))
        self.assertEqual(launch_persona.extract_receipt(""), (None, None))


class WorkerStart(unittest.TestCase):
    """O fluxo real com `run_fn` falso: nenhum comando do brza roda."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.mapa = os.path.join(self.tmp, "s", "sessions.jsonl")
        self.p = REUNIAO["personas"][0]

    def roda(self, rc, out, **kw):
        chamadas = []

        def run_fn(argv):
            chamadas.append(argv)
            return rc, out, "erro"
        with redirect_stderr(io.StringIO()) as err, redirect_stdout(io.StringIO()):
            r = launch_persona.start_worker(REUNIAO, self.p, self.tmp, "worker-start", self.mapa, run_fn=run_fn, **kw)
        return r, chamadas, err.getvalue()

    def test_grava_recibo_e_linha_open(self):
        r, chamadas, _ = self.roda(0, '{"dispatch_id": "d1", "orca_session_id": "t1"}')
        self.assertEqual(r, 0)
        self.assertEqual(chamadas[0][:3], ["brza", "orchestration", "worker-start"])
        log = launch_persona.log_path(REUNIAO, self.p, self.tmp)
        self.assertIn("d1", _le(log))
        linha = json.loads(_le(self.mapa))
        self.assertEqual((linha["event"], linha["via"], linha["dispatch_id"], linha["orca_session_id"], linha["name"]),
                         ("open", "worker-start", "d1", "t1", self.p["sessao"]))
        self.assertIn("title", linha)
        self.assertRegex(linha["at"], r"T\d\d:\d\d:\d\d[+-]\d\d:\d\d$")

    def test_recibo_sem_ids_grava_null_e_avisa(self):
        r, _, err = self.roda(0, '{"x": 1}')
        self.assertEqual(r, 0)
        linha = json.loads(_le(self.mapa))
        self.assertIsNone(linha["dispatch_id"])
        self.assertIsNone(linha["orca_session_id"])
        self.assertIn("launch-", err)

    def test_worker_start_avisa_que_o_mapa_nao_acha_a_persona(self):
        """B2a: a linha `open` do worker-start não tem chat/claude_session/provider_session."""
        _, _, err = self.roda(0, '{"dispatch_id": "d1", "orca_session_id": "t1"}')
        self.assertIn("NÃO acharão esta persona até a sonda P4a.0", err)
        self.assertIn("`brza sessions send/list`", err)
        linha = json.loads(_le(self.mapa))
        for k in ("chat", "claude_session", "provider_session"):
            self.assertNotIn(k, linha)

    def test_falha_nao_grava_no_mapa(self):
        r, _, err = self.roda(3, "")
        self.assertEqual(r, 3)
        self.assertFalse(os.path.exists(self.mapa))
        self.assertIn("falhou", err)


if __name__ == "__main__":
    unittest.main()


class CheckoutRelativoARaizComum(unittest.TestCase):
    def test_checkout_nao_dobra_o_caminho_dentro_de_um_worktree(self):
        import launch_persona as lp
        raiz = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *(['..'] * 5)))
        r = lp.checkout_abs({"checkout": ".worktrees/playground"}, raiz)
        self.assertFalse(r.endswith(".worktrees/playground/.worktrees/playground"), r)
        self.assertTrue(r.endswith("/.worktrees/playground"), r)

    def test_checkout_absoluto_fica(self):
        import launch_persona as lp
        self.assertEqual(lp.checkout_abs({"checkout": "/x/y"}, "/tmp"), "/x/y")
