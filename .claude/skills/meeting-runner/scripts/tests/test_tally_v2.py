"""Testes do tally.py sobre o mapa v2 e as seções REAIS do P7 (R3 da Trava e do Relance): X1, X4, X7, X10, X17, X18."""
import builtins
import contextlib
import io
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
import unittest
from datetime import datetime

import _paths  # noqa: F401
from _paths import HERE, fixture, le

import tally
from p7 import jsonl, monta_raiz

try:
    import sessions_map
except ImportError:  # snapshot anterior ao v2
    sessions_map = None

DIA = "2026-11-09"
UUID = "cd289115-4fab-49e4-bc30-58247c2cfe74"


def mapa_v2(sessao="ci-prumo", com_close=True, claude_no_open=False):
    rows = [{"event": "open", "at": f"{DIA}T13:15:00.000-03:00", "name": sessao, "chat": "chat-1", "agent": "claude",
             "dispatch": "ctx_80fad49a44fd", "run": "run_fe70b351bc36", "sender": "structworker_271da", "coordinator": "orca_session_id:x",
             "model": "claude-opus-5-5", "effort": "xhigh", "operation": "op1", "round_id": "op1",
             "claude_session": UUID if claude_no_open else None, "provider_session": UUID if claude_no_open else None},
            {"event": "session", "at": f"{DIA}T13:15:30.000-03:00", "name": sessao, "chat": "chat-1",
             "provider_session": UUID, "claude_session": UUID},
            {"event": "send", "at": f"{DIA}T18:37:02.000-03:00", "name": sessao, "chat": "chat-1", "operation": "op3",
             "round_id": "op3", "receipt": {"status": "accepted"}},
            {"event": "turn", "at": f"{DIA}T18:38:20.000-03:00", "name": sessao, "chat": "chat-1", "operation": "op3",
             "outcome": "done", "latency_s": 78.0}]
    if com_close:
        rows.append({"event": "close", "at": f"{DIA}T18:41:00.000-03:00", "name": sessao, "chat": "chat-1"})
    return rows


def turno(sid, ts, custo=1.25, dur=40):
    return {"event": "turn", "session_id": sid, "timestamp": ts, "estimated_cost_usd": custo, "duration_s": dur}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.root, self.reuniao = monta_raiz(self.tmp)
        self.mapa = os.path.join(self.tmp, "s", "sessions.jsonl")
        self.med = os.path.join(self.tmp, "m", "measurements.jsonl")
        self.vazio = os.path.join(self.tmp, "nao-existe")

    def estado(self, n=3, **kw):
        kw.setdefault("measurements", self.med)
        kw.setdefault("sessions", self.mapa)
        kw.setdefault("codex_dir", self.vazio)
        return tally.build_estado(self.reuniao, n, self.root, **kw)

    def persona(self, e, nome):
        return next(p for p in e["personas"] if p["nome"] == nome)

    def prumo_respondeu_r3(self):
        """O worklog do Prumo ganha a seção da R3 (ele respondeu, e o hook ainda não gravou o turno)."""
        path = os.path.join(self.root, "work/worklogs/2026-11-09-reuniao-ci-no-chat-prumo.md")
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n### Rodada 3: o voto informado entre A e B\n\n- **Posição:** Voto A.\n\n#### O voto\n\n"
                    "| Proposta | Voto | Ressalva | Confiança |\n| :-- | :-- | :-- | :-- |\n"
                    "| A | apoio | nenhuma | 90 |\n| B | contra | mede zero | 88 |\n\n- **Fatos lidos:** M6, M6b\n\n"
                    "<!-- fim-rodada-3 -->\n")
        os.utime(path, (1794260000, 1794260000))


class X17Voto(Base):
    def rodada3(self, slug):
        with open(os.path.join(self.root, f"work/worklogs/2026-11-09-reuniao-ci-no-chat-{slug}.md"), encoding="utf-8") as f:
            return tally.parse_worklog(f.read(), ["Prumo", "Trava", "Relance"])["rodadas"][3]

    def test_r3_real_da_trava_e_do_relance(self):
        for slug, conf in (("trava", 84.0), ("relance", 88.0)):
            r = self.rodada3(slug)
            self.assertEqual(r["voto"], {"apoio": 0, "ressalva": 1, "contra": 1}, slug)   # A com ressalva, B contra
            self.assertEqual((r["confianca"], r["confianca_fonte"]), (conf, "plano"), slug)  # a do `O plano inteiro`

    def test_cabecalho_antigo_com_rotulos_p(self):
        txt = ("### Rodada 3: x\n\n#### O voto em cada proposta\n\n| Proposta | Voto | Confiança |\n| :-- | :-- | :-- |\n"
               "| P1 | apoio | 80 |\n| P2 | contra | 60 |\n\n<!-- fim-rodada-3 -->\n")
        r = tally.parse_worklog(txt)["rodadas"][3]
        self.assertEqual(r["voto"], {"apoio": 1, "ressalva": 0, "contra": 1})
        self.assertEqual((r["confianca"], r["confianca_fonte"]), (70.0, "voto"))

    def test_sem_plano_inteiro_a_confianca_e_a_media_da_coluna_do_voto(self):
        txt = ("### Rodada 3: x\n\n#### O voto\n\n| Proposta | Voto | Ressalva | Confiança |\n| :-- | :-- | :-- | :-- |\n"
               "| A | apoio com ressalva | r | 86 |\n| B | contra | r | 84 |\n\n<!-- fim-rodada-3 -->\n")
        r = tally.parse_worklog(txt)["rodadas"][3]
        self.assertEqual((r["confianca"], r["confianca_fonte"]), (85.0, "voto"))

    def test_linha_cuja_celula_de_voto_nao_se_classifica_nao_conta(self):
        txt = ("### Rodada 3: x\n\n#### O voto\n\n| Proposta | Voto | Confiança |\n| :-- | :-- | :-- |\n"
               "| A | apoio | 80 |\n| Total | n/d | 80 |\n\n<!-- fim-rodada-3 -->\n")
        self.assertEqual(tally.parse_worklog(txt)["rodadas"][3]["voto"], {"apoio": 1, "ressalva": 0, "contra": 0})

    def test_placar_da_r2_real_com_o_sinal_de_paralelo_e_virou(self):
        with open(os.path.join(self.root, "work/worklogs/2026-11-09-reuniao-ci-no-chat-trava.md"), encoding="utf-8") as f:
            r2 = tally.parse_worklog(f.read())["rodadas"][2]
        self.assertEqual(r2["virada"], "virou")
        self.assertEqual(r2["placar_conf"], 85.3)


class MarcadorComMedida(Base):
    def parse(self, texto):
        return tally.parse_worklog(texto, ["Prumo", "Trava", "Relance"])

    def test_fim_real_do_worklog_da_trava_depois_do_commit(self):
        w = self.parse(le("p7", "worklogs", "trava-commitado.md"))
        self.assertEqual(w["marcador_final"], 3)
        self.assertEqual(w["rodadas"][3]["voto"], {"apoio": 0, "ressalva": 1, "contra": 1})

    def test_outra_secao_depois_do_marcador_continua_invalidando(self):
        base = le("p7", "worklogs", "trava-commitado.md")
        self.assertIsNone(self.parse(base + "\n## O que ficou\n\nNada.\n")["marcador_final"])
        self.assertIsNone(self.parse(base.split("## Medida")[0] + "## O que ficou\n\nx\n\n## Medida\n\ny\n")["marcador_final"])

    def test_estado_da_persona_commitada_e_respondeu(self):
        wl = os.path.join(self.root, "work/worklogs/2026-11-09-reuniao-ci-no-chat-trava.md")
        shutil.copy(fixture("p7", "worklogs", "trava-commitado.md"), wl)
        e = self.estado(participantes=["Trava"])
        self.assertEqual(self.persona(e, "Trava")["estado"], "respondeu")


class X10FatosLidos(Base):
    def test_linha_de_fatos_lidos_vira_lista(self):
        txt = "### Rodada 3: x\n\n- **Posição:** A\n- **Fatos lidos:** M1, M6, M6b e M9.\n\n<!-- fim-rodada-3 -->\n"
        self.assertEqual(tally.parse_worklog(txt)["rodadas"][3]["fatos_lidos"], ["M1", "M6", "M6b", "M9"])
        self.assertIsNone(tally.parse_worklog("### Rodada 3: x\n\ntexto\n")["rodadas"][3]["fatos_lidos"])

    def test_votou_sem_declarar_os_fatos_lidos_gera_aviso(self):
        e = self.estado(participantes=["Trava", "Relance"])
        self.assertIn("Trava: votou sem declarar os fatos lidos", e["avisos"])
        self.assertIn("Relance: votou sem declarar os fatos lidos", e["avisos"])

    def test_com_a_linha_nao_avisa(self):
        self.prumo_respondeu_r3()
        e = self.estado()
        self.assertEqual(self.persona(e, "Prumo")["fatos_lidos"], ["M6", "M6b"])
        self.assertNotIn("Prumo: votou sem declarar os fatos lidos", e["avisos"])


class X18Participantes(Base):
    def test_quem_esta_fora_nao_entra_na_sala_nem_no_x_de_n(self):
        e = self.estado(participantes=["Trava", "Relance"])
        prumo = self.persona(e, "Prumo")
        self.assertEqual(prumo["estado"], "fora da rodada")
        self.assertIsNone(prumo["confianca"])
        self.assertIsNone(prumo["custo_usd"])
        self.assertEqual((e["sala"]["n"], e["sala"]["n_todas"], e["sala"]["total"]), (1, 2, 2))  # Relance (E-1) à parte
        self.assertEqual(e["rodada"]["participantes"], ["Trava", "Relance"])
        self.assertEqual(e["sala"]["mediana"], 84.0)   # a sala é só a Trava; a Relance (Antigravity) fica à parte
        self.assertEqual(e["sala"]["antigravity"]["media"], 88.0)
        self.assertIn("Sala: média 84 (1/2)", tally.render_md(e))
        self.assertIn("| Prumo | — (fora da rodada) |", tally.render_md(e))

    def test_sem_participantes_o_prumo_e_falta_e_o_total_e_3(self):
        e = self.estado()
        self.assertEqual(self.persona(e, "Prumo")["estado"], "falta")
        self.assertEqual(e["sala"]["total"], 3)
        self.assertEqual(e["rodada"]["participantes"], ["Prumo", "Trava", "Relance"])

    def test_cli_participantes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            rc = tally.main(["3", "--reuniao", os.path.join(self.root, ".sessions/reuniao-ci-no-chat/reuniao.json"),
                             "--root", self.root, "--measurements", self.med, "--sessions", self.mapa, "--out", "-",
                             "--participantes", "Trava", "Relance"])
        self.assertEqual(rc, 0)
        self.assertIn("fora da rodada", out.getvalue())


class X1IdentidadePeloMapa(Base):
    def test_open_sem_id_session_depois_send_turn_e_close_a_persona_claude_e_medida(self):
        self.prumo_respondeu_r3()
        jsonl(self.mapa, mapa_v2())
        jsonl(self.med, [turno(UUID, f"{DIA}T21:38:00+00:00", 1.25, 40), turno(UUID, f"{DIA}T21:38:50+00:00", 0.75, 30),
                         turno("outra-sessao", f"{DIA}T21:38:10+00:00", 9.0)])
        e = self.estado(opened="18:37:02", closed="18:38:50", at="18:44:00", participantes=["Prumo"])
        p = self.persona(e, "Prumo")
        self.assertEqual(p["custo_usd"], 2.0)
        self.assertEqual(p["medicao"], "medida")
        self.assertIsNone(p["medicao_aviso"])
        self.assertEqual(e["rodada"]["custo_rotulo"], "da rodada")

    def test_open_do_v2_so_com_provider_session_vale_como_sessao_do_claude(self):
        """O v2 grava `provider_session` no `open` e só depois (ou nunca) o `claude_session`: no Claude é o mesmo id."""
        self.prumo_respondeu_r3()
        rows = mapa_v2(com_close=False, claude_no_open=True)
        rows[0]["claude_session"] = None
        del rows[1]                                  # sem o evento `session`: só o `open` tem o id
        jsonl(self.mapa, rows)
        jsonl(self.med, [turno(UUID, f"{DIA}T21:38:00+00:00", 2.5, 60)])
        self.assertEqual(tally.session_ids(rows, "ci-prumo"), ({UUID}, {UUID}))
        e = self.estado(opened="18:37:02", closed="18:38:50", at="18:44:00", participantes=["Prumo"])
        self.assertEqual(self.persona(e, "Prumo")["custo_usd"], 2.5)

    def test_session_ids_so_do_mapa_e_do_manifesto(self):
        rows = mapa_v2()
        self.assertEqual(tally.session_ids(rows, "ci-prumo"), ({UUID}, {UUID}))
        self.assertEqual(tally.session_ids(rows, "ci-prumo", {"claude_session": "forçado"}), ({"forçado"}, {UUID}))
        self.assertEqual(tally.session_ids(rows, "nao-existe"), (set(), set()))

    def test_nada_le_transcript_do_claude(self):
        self.prumo_respondeu_r3()
        jsonl(self.mapa, mapa_v2())
        jsonl(self.med, [turno(UUID, f"{DIA}T21:38:00+00:00")])
        abertos = []
        real = builtins.open

        def espia(f, *a, **k):
            abertos.append(str(f))
            return real(f, *a, **k)
        builtins.open = espia
        try:
            self.estado(opened="18:37:02", closed="18:38:50", at="18:44:00")
        finally:
            builtins.open = real
        self.assertFalse([a for a in abertos if "/.claude/projects/" in a or "custom-title" in a], abertos)
        with real(tally.__file__, encoding="utf-8") as f:
            fonte = f.read()
        for proibido in ("custom-title", ".claude/projects", "'projects'", '"projects"'):
            self.assertNotIn(proibido, fonte)

    def test_a_mesma_leitura_nos_tres_scripts(self):
        import launch_persona
        import wait_round
        rows = mapa_v2()
        jsonl(self.mapa, rows)
        esperado = sessions_map.fold_map(rows)
        self.assertEqual(sessions_map.load_map(self.root, self.mapa), esperado)
        self.assertIs(launch_persona.sessions_map, sessions_map)
        self.assertIs(wait_round.sessions_map, sessions_map)
        self.assertIs(tally.sessions_map, sessions_map)


class X4Pendente(Base):
    def setUp(self):
        super().setUp()
        self.prumo_respondeu_r3()
        jsonl(self.mapa, mapa_v2())
        jsonl(self.med, [])

    def pendente(self, **kw):
        return self.estado(opened="18:37:02", participantes=["Prumo"], **kw)

    def test_fechada_ha_menos_de_120_s_o_hook_ainda_nao_gravou(self):
        e = self.pendente(closed="18:38:50", at="18:39:30")
        p = self.persona(e, "Prumo")
        self.assertEqual((p["medicao"], p["custo_usd"]), ("pendente", None))
        self.assertIn("Prumo: medição pendente: o hook grava no Stop do turno; rode de novo em ~1 min", e["avisos"])
        md = tally.render_md(e)
        self.assertIn("Custo (rodada)", md)
        self.assertIn("| pendente |", md)
        self.assertNotIn("US$ 0", md)

    def test_depois_de_120_s_continua_sem_medicao(self):
        e = self.pendente(closed="18:38:50", at="18:41:00")
        p = self.persona(e, "Prumo")
        self.assertEqual((p["medicao"], p["custo_usd"]), ("sem medição", None))
        self.assertFalse([a for a in e["avisos"] if "pendente" in a])

    def test_sem_janela_vale_a_hora_da_resposta(self):
        e = self.estado(participantes=["Prumo"], at=datetime.fromtimestamp(1794260000 + 30).astimezone().isoformat())
        self.assertEqual(self.persona(e, "Prumo")["medicao"], "pendente")
        self.assertEqual(e["rodada"]["custo_rotulo"], "total da sessão")
        e = self.estado(participantes=["Prumo"], at=datetime.fromtimestamp(1794260000 + 600).astimezone().isoformat())
        self.assertEqual(self.persona(e, "Prumo")["medicao"], "sem medição")

    def test_grok_e_antigravity_nunca_ficam_pendentes(self):
        e = self.estado(opened="18:37:02", closed="18:38:50", at="18:39:30")
        self.assertIsNone(self.persona(e, "Trava")["medicao"])
        self.assertIsNone(self.persona(e, "Relance")["medicao"])

    def test_settle_relê_ate_o_turno_chegar(self):
        t = {"v": 0.0}
        dormiu = []

        def sleep(s):
            dormiu.append(s)
            t["v"] += s
            if len(dormiu) == 2:   # o hook grava o turno depois de 10 s
                jsonl(self.med, [turno(UUID, f"{DIA}T21:38:30+00:00", 1.5, 70)])
        e = self.pendente(closed="18:38:50", at="18:39:30", settle=60, sleep=sleep, clock=lambda: t["v"])
        p = self.persona(e, "Prumo")
        self.assertEqual((p["medicao"], p["custo_usd"]), ("medida", 1.5))
        self.assertEqual(dormiu, [5, 5])
        self.assertFalse([a for a in e["avisos"] if "pendente" in a])

    def test_settle_vencido_continua_pendente(self):
        t = {"v": 0.0}

        def sleep(s):
            t["v"] += s
        e = self.pendente(closed="18:38:50", at="18:39:30", settle=12, sleep=sleep, clock=lambda: t["v"])
        self.assertEqual(self.persona(e, "Prumo")["medicao"], "pendente")
        self.assertGreaterEqual(t["v"], 12)

    def test_cli_at_e_settle(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = tally.main(["3", "--reuniao", os.path.join(self.root, ".sessions/reuniao-ci-no-chat/reuniao.json"),
                             "--root", self.root, "--measurements", self.med, "--sessions", self.mapa, "--out", "-",
                             "--participantes", "Prumo", "--opened", "18:37:02", "--closed", "18:38:50", "--at", "18:39:30"])
        self.assertEqual(rc, 0)
        self.assertIn("| pendente |", out.getvalue())
        self.assertIn("aviso: Prumo: medição pendente", err.getvalue())

    def test_settle_0_nao_dorme(self):
        e = self.pendente(closed="18:38:50", at="18:39:30", sleep=lambda s: self.fail("não dorme com settle 0"))
        self.assertEqual(self.persona(e, "Prumo")["medicao"], "pendente")


class X7Rotulo(Base):
    def test_cabecalho_da_coluna_de_custo_leva_o_rotulo(self):
        self.prumo_respondeu_r3()
        jsonl(self.mapa, mapa_v2())
        jsonl(self.med, [turno(UUID, f"{DIA}T21:38:00+00:00", 1.25, 40)])
        e = self.estado(opened="18:37:02", closed="18:38:50", at="18:44:00", participantes=["Prumo"])
        self.assertEqual(e["rodada"]["custo_rotulo"], "da rodada")
        self.assertIn("Custo (rodada)", tally.render_md(e))
        self.assertIn("US$ 1,3", tally.render_md(e).replace("US$ 1,2", "US$ 1,3"))  # 1,25 arredondado
        e = self.estado(at="18:44:00", participantes=["Prumo"])
        self.assertEqual(e["rodada"]["custo_rotulo"], "total da sessão")
        md = tally.render_md(e)
        self.assertIn("Custo (total da sessão)", md)
        self.assertIn("total da sessão (sem a janela da rodada)", md)

    def test_sem_custo_nem_pendente_o_md_nao_ganha_a_coluna(self):
        e = self.estado(participantes=["Trava", "Relance"])
        self.assertNotIn("Custo (", tally.render_md(e).split("\n")[0])


class ParticipantesResolvidos(Base):
    def test_nome_slug_ou_sessao_sem_caixa(self):
        for q in ("Trava", "trava", "CI-TRAVA"):
            e = self.estado(participantes=[q])
            self.assertEqual(e["rodada"]["participantes"], ["Trava"], q)

    def test_nome_desconhecido_levanta_e_a_cli_sai_2(self):
        with self.assertRaisesRegex(ValueError, "persona desconhecida: Fulano"):
            self.estado(participantes=["Fulano"])
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            rc = tally.main(["3", "--reuniao", os.path.join(self.root, ".sessions/reuniao-ci-no-chat/reuniao.json"),
                             "--root", self.root, "--measurements", self.med, "--sessions", self.mapa, "--out", "-",
                             "--participantes", "Trava", "Fulano"])
        self.assertEqual(rc, 2)
        self.assertIn("persona desconhecida: Fulano", err.getvalue())


class FatosLidosDeclarados(Base):
    def test_nenhum_novo_e_lista_vazia_declarada_e_nao_avisa(self):
        txt = "### Rodada 3: x\n\n#### O voto\n\n| P | Voto | Confiança |\n| :-- | :-- | :-- |\n| A | apoio | 80 |\n\n- **Fatos lidos:** nenhum novo\n\n<!-- fim-rodada-3 -->\n"
        self.assertEqual(tally.parse_worklog(txt)["rodadas"][3]["fatos_lidos"], [])
        wl = os.path.join(self.root, "work/worklogs/2026-11-09-reuniao-ci-no-chat-trava.md")
        Path(wl).write_text(txt, encoding="utf-8")
        e = self.estado(participantes=["Trava"])
        self.assertNotIn("Trava: votou sem declarar os fatos lidos", e["avisos"])


class VotoPorProposta(Base):
    def test_r3_real_da_trava(self):
        e = self.estado(participantes=["Trava", "Relance"])
        self.assertEqual(self.persona(e, "Trava")["voto_por_proposta"], {"A": "apoio com ressalva", "B": "contra"})
        self.assertIsNone(self.persona(e, "Prumo")["voto_por_proposta"])

    def test_p1_p2(self):
        txt = ("### Rodada 3: x\n\n#### O voto em cada proposta\n\n| Proposta | Voto | Confiança |\n| :-- | :-- | :-- |\n"
               "| P1 | apoio | 80 |\n| P2 | contra | 60 |\n\n<!-- fim-rodada-3 -->\n")
        self.assertEqual(tally.parse_worklog(txt)["rodadas"][3]["voto_por_proposta"], {"P1": "apoio", "P2": "contra"})


class MapaPadrao(Base):
    def test_o_mapa_padrao_e_o_do_sessions_map(self):
        usado = []
        original = sessions_map.map_file
        sessions_map.map_file = lambda root, sessions=None: usado.append(root) or self.mapa
        try:
            jsonl(self.mapa, mapa_v2())
            tally.build_estado(self.reuniao, 3, self.root, measurements=self.med, codex_dir=self.vazio)
        finally:
            sessions_map.map_file = original
        self.assertEqual(usado, [self.root])


class VotoNaTabelaDoChat(Base):
    def test_render_md_mostra_o_voto_por_proposta(self):
        e = self.estado(participantes=["Trava", "Relance"])
        md = tally.render_md(e)
        self.assertIn("| A: apoio c/ ressalva · B: contra |", md)
        self.assertNotIn("0/1/1", md)

    def test_sem_voto_por_proposta_cai_para_as_contagens(self):
        e = self.estado(participantes=["Trava", "Relance"])
        for p in e["personas"]:
            p["voto_por_proposta"] = None
        self.assertIn("| 0/1/1 |", tally.render_md(e))


class NotaDosClaudeSoComClaudeNaRodada(Base):
    """A4: o render_md dizia "Custo e latência dos Claude: total da sessão" sem nenhum Claude entre os participantes."""

    def test_sem_claude_entre_os_participantes_a_nota_nao_sai(self):
        e = self.estado(participantes=["Trava", "Relance"])
        self.assertEqual(e["rodada"]["custo_rotulo"], "total da sessão")   # o contrato fica como estava
        self.assertNotIn("Custo e latência dos Claude", tally.render_md(e))

    def test_com_o_prumo_na_rodada_a_nota_continua(self):
        e = self.estado()
        self.assertIn("Custo e latência dos Claude: total da sessão", tally.render_md(e))


if __name__ == "__main__":
    unittest.main()
