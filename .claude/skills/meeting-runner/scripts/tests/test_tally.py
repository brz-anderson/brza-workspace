"""Testes do tally.py: o aceite com os worklogs reais de 2026-11-07 e a medição com fixtures sintéticas.

Rodar: cd .claude/skills/meeting-runner && python3 -I -m unittest discover -s scripts/tests -p 'test_tally.py'
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import tally  # noqa: E402

FIX = os.path.join(HERE, "fixtures")


def load(nome):
    with open(os.path.join(FIX, nome), encoding="utf-8") as f:
        return json.load(f)


def raiz_do_repo():
    """O worktree do playground: `.claude/skills/meeting-runner/scripts/tests` está 5 níveis abaixo dele."""
    if os.environ.get("MR_ROOT"):
        return os.environ["MR_ROOT"]
    r = HERE
    for _ in range(5):
        r = os.path.dirname(r)
    return r


class AceiteComOsWorklogsReais(unittest.TestCase):
    """Refaz as tabelas por persona do levantamento (seções 3.1 e 3.2) que dependem só dos worklogs."""

    @classmethod
    def setUpClass(cls):
        cls.root = raiz_do_repo()
        if not os.path.isfile(os.path.join(cls.root, "work/worklogs/2026-11-07-reuniao-mcp-remoto-muralha.md")):
            raise unittest.SkipTest("work/worklogs de 2026-11-07 não existem neste checkout")
        cls.mcp, cls.carvao = load("reuniao-mcp-remoto.json"), load("reuniao-carvao.json")
        cls.vazio = os.path.join(FIX, "inexistente")  # sem medição: só o que sai dos worklogs

    def estado(self, reuniao, n, **kw):
        e = tally.build_estado(reuniao, n, self.root, measurements=self.vazio, sessions=self.vazio,
                               codex_dir=self.vazio, **kw)
        return {p["nome"]: p for p in e["personas"]}, e

    def col(self, ps, campo):
        return {nome: p[campo] for nome, p in ps.items()}

    def test_confianca_r1_media_mcp(self):
        ps, _ = self.estado(self.mcp, 1)
        self.assertEqual(self.col(ps, "confianca_r1"), {"Muralha": 72.5, "Régua": 78.8, "Atalho": 77.5,
                                                         "Salto": 63.8, "Plantão": 55.0, "Cartógrafo": 83.8})

    def test_confianca_r1_media_carvao(self):
        ps, _ = self.estado(self.carvao, 1)
        self.assertEqual(self.col(ps, "confianca_r1"), {"Tição": 73.0, "Faísca": 70.4, "Cinza": 79.4, "Lenha": 86.6,
                                                         "Fogareiro": 89.0, "Fole": 68.0})

    def test_confianca_por_rodada_mcp(self):
        esperado = {3: [58, 68, 55, 55, 50, 85], 4: [72, 76, 65, 64, 55, 88],
                    5: [74, None, 75, 68, 50, 85], 6: [66, None, None, 60, 45, 88]}
        for n, vals in esperado.items():
            ps, _ = self.estado(self.mcp, n)
            self.assertEqual([p["confianca"] for p in ps.values()],
                             [None if v is None else float(v) for v in vals], f"R{n}")

    def test_confianca_por_rodada_carvao(self):
        esperado = {3: [78.5, 76.3, 92.0, 93.4, 92.9, 75.7],      # média da coluna Confiança do voto
                    5: [76, 64, 77, 81, 88, 74], 7: [80, 81, 88, 90, 94, 82]}
        for n, vals in esperado.items():
            ps, _ = self.estado(self.carvao, n)
            self.assertEqual([p["confianca"] for p in ps.values()], [float(v) for v in vals], f"R{n}")
        ps, _ = self.estado(self.carvao, 4)  # rodada de entrega: sem confiança, e sem exceção
        self.assertTrue(all(p["confianca"] is None for p in ps.values()))

    def test_voto_r3_carvao(self):
        ps, e = self.estado(self.carvao, 3)
        esperado = {"Tição": (8, 7, 0), "Faísca": (2, 11, 2), "Cinza": (2, 7, 6), "Lenha": (3, 11, 1),
                    "Fogareiro": (12, 3, 0), "Fole": (10, 5, 0)}
        for nome, (a, r, c) in esperado.items():
            self.assertEqual(ps[nome]["voto"], {"apoio": a, "ressalva": r, "contra": c}, nome)
        self.assertTrue(e["rodada"]["tem_voto"])
        ps, e = self.estado(self.mcp, 3)  # a MCP não tem voto
        self.assertTrue(all(p["voto"] is None for p in ps.values()))
        self.assertFalse(e["rodada"]["tem_voto"])

    def test_nota_dos_colegas_carvao_recalculada(self):
        ps, _ = self.estado(self.carvao, 3)
        esperado = {"Tição": 8.5, "Faísca": 8.8, "Cinza": 9.1, "Lenha": 8.3, "Fogareiro": 6.6, "Fole": 8.4}
        for nome, v in esperado.items():
            self.assertAlmostEqual(ps[nome]["nota_colegas"], v, delta=0.05, msg=nome)
            self.assertEqual(ps[nome]["nota_rodada"], 3)

    def test_nota_dos_colegas_carvao_sem_a_faisca(self):
        """F13: a conta da coordenação (coordB:97-102) só bate sem as notas que a Faísca deu."""
        ps, _ = self.estado(self.carvao, 3, exclude_raters=("Faísca",))
        self.assertAlmostEqual(ps["Tição"]["nota_colegas"], 8.9, delta=0.05)    # 8,875
        self.assertAlmostEqual(ps["Fogareiro"]["nota_colegas"], 6.25, delta=0.001)
        self.assertAlmostEqual(ps["Fole"]["nota_colegas"], 8.25, delta=0.001)

    def test_nota_dos_colegas_mcp(self):
        ps, _ = self.estado(self.mcp, 3)
        esperado = {"Régua": 9.4, "Muralha": 9.0, "Atalho": 6.6, "Salto": 6.2, "Plantão": 7.8, "Cartógrafo": 6.0}
        for nome, v in esperado.items():
            self.assertAlmostEqual(ps[nome]["nota_colegas"], v, delta=0.05, msg=nome)

    def test_sala_r3_mcp(self):
        _, e = self.estado(self.mcp, 3)
        s = e["sala"]
        self.assertEqual((s["media_todas"], s["mediana_todas"], s["n_todas"]), (61.8, 56.5, 6))
        self.assertEqual((s["media"], s["n"]), (57.2, 5))  # sem o Cartógrafo (E-1)
        self.assertEqual(s["antigravity"], {"media": 85.0, "n": 1, "nomes": ["Cartógrafo"], "fora_da_media": True})

    def test_linha_e_posicao(self):
        ps, _ = self.estado(self.mcp, 3)
        with open(os.path.join(self.root, ps["Muralha"]["worklog"]), encoding="utf-8") as f:
            linhas = f.read().split("\n")
        self.assertTrue(linhas[ps["Muralha"]["linha"] - 1].startswith("### Rodada 3"))
        for p in ps.values():
            self.assertLessEqual(len(p["posicao"]), 100)

    def test_marcador_na_ultima_linha(self):
        """A R6 da MCP termina em fim-rodada-6 em quatro das seis; Régua parou na 4 e Atalho na 5."""
        ps, _ = self.estado(self.mcp, 6)
        self.assertEqual({n: p["estado"] for n, p in ps.items()},
                         {"Muralha": "respondeu", "Régua": "falta", "Atalho": "falta", "Salto": "respondeu",
                          "Plantão": "respondeu", "Cartógrafo": "respondeu"})


class ParseWorklog(unittest.TestCase):
    def test_secao_ausente_vira_none(self):
        w = tally.parse_worklog("# t\n\n## O que se fez\n\n### Rodada 2: debate\n\nsó texto\n")
        r = w["rodadas"][2]
        self.assertIsNone(r["confianca"])
        self.assertIsNone(r["voto"])
        self.assertIsNone(r["notas"])
        self.assertIsNone(r["posicao"])
        self.assertIsNone(w["marcador_final"])
        self.assertEqual(tally.parse_worklog("")["rodadas"], {})

    def test_marcador_so_vale_na_ultima_linha(self):
        meio = tally.parse_worklog("### Rodada 1: a\n\n<!-- fim-rodada-1 -->\n\n## O que ficou\n\nNada.\n")
        self.assertIsNone(meio["marcador_final"])
        self.assertEqual(meio["marcadores"], [1])
        fim = tally.parse_worklog("### Rodada 1: a\n\n<!-- fim-rodada-1 -->\n\n\n")
        self.assertEqual(fim["marcador_final"], 1)
        quase = tally.parse_worklog("### Rodada 1: a\n\n<!-- fim-rodada-1 --> \n")
        self.assertEqual(quase["marcador_final"], 1)  # espaço no fim da linha é tolerado

    def test_posicao_corta_em_100(self):
        w = tally.parse_worklog("### Rodada 1: a\n\n- **Posição:** " + "x" * 300 + "\n")
        p = w["rodadas"][1]["posicao"]
        self.assertEqual(len(p), 100)
        self.assertTrue(p.endswith("…"))

    def test_posicao_junta_a_continuacao_e_tira_enfase(self):
        w = tally.parse_worklog("### Rodada 1: a\n\n- **Posição:** *suposto* — A + D\n  segue na linha de baixo.\n- outro\n")
        self.assertEqual(w["rodadas"][1]["posicao"], "A + D segue na linha de baixo.")

    def test_notas_em_prosa_e_tabela(self):
        prosa = ("### Rodada 3: x\n\n- **Nota aos colegas:** *avaliação* (70/100): Muralha 9/10 — a; "
                 "Régua 10/10 — b; Salto 8,5 (c)\n\n<!-- fim-rodada-3 -->\n")
        self.assertEqual(tally.parse_worklog(prosa, ["Muralha", "Régua", "Salto"])["rodadas"][3]["notas"],
                         {"Muralha": 9.0, "Régua": 10.0, "Salto": 8.5})
        lista = "### Rodada 3: x\n\n- **Nota aos colegas:**\n  - **Régua (10/10):** r\n  - Muralha — 9/10: m\n\nfim\n"
        self.assertEqual(tally.parse_worklog(lista, ["Muralha", "Régua"])["rodadas"][3]["notas"],
                         {"Régua": 10.0, "Muralha": 9.0})
        tabela = ("### Rodada 3: x\n\n#### Os colegas\n\n| Persona | A contribuição | Nota de 0 a 10 |\n"
                  "| :-- | :-- | :-- |\n| Faísca | os fatos | 8 |\n| Cinza | o piloto | 9 |\n")
        self.assertEqual(tally.parse_worklog(tabela)["rodadas"][3]["notas"], {"Faísca": 8.0, "Cinza": 9.0})

    def test_plano_inteiro_pega_a_ultima_celula_numerica(self):
        txt = ("### Rodada 4: x\n\n| Parte | v1 | v2 | porquê |\n| :-- | :-- | :-- | :-- |\n"
               "| **O plano inteiro** | **58** | **72** | agora sim |\n")
        r = tally.parse_worklog(txt)["rodadas"][4]
        self.assertEqual((r["confianca"], r["confianca_fonte"], r["posicao"]), (72.0, "plano", "agora sim"))


class Medicao(unittest.TestCase):
    """Fixtures sintéticas: measurements.jsonl de 3 linhas, sessions.jsonl, dois rollouts do Codex."""

    def setUp(self):
        self._tz = os.environ.get("TZ")
        os.environ["TZ"] = "America/Sao_Paulo"
        time.tzset()
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.addCleanup(self._restaura_tz)
        self.reuniao = load("reuniao-mcp-remoto.json")
        os.makedirs(os.path.join(self.tmp, "work/worklogs"))
        marcado = lambda plano: (f"## O que se fez\n\n### Rodada 3: a confiança no plano\n\n| Parte | Confiança | Porquê |\n"
                                 f"| :-- | :-- | :-- |\n| **O plano inteiro** | {plano} | porque {plano} |\n\n"
                                 f"<!-- fim-rodada-3 -->\n")
        escreve = {"muralha": marcado(58), "regua": marcado(68), "salto": marcado(55), "plantao": marcado(50),
                   # Atalho: gravou a seção mas o turno morreu no limite, sem marcador
                   "atalho": "## O que se fez\n\n### Rodada 3: a confiança no plano\n\nparcial\n"}
        for slug, texto in escreve.items():
            with open(os.path.join(self.tmp, f"work/worklogs/2026-11-07-reuniao-mcp-remoto-{slug}.md"), "w") as f:
                f.write(texto)
        self.set_mtime("salto", "2026-11-07T21:29:00-03:00")
        self.set_mtime("plantao", "2026-11-07T21:29:30-03:00")

    def _restaura_tz(self):
        if self._tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = self._tz
        time.tzset()

    def set_mtime(self, slug, iso):
        ts = datetime.fromisoformat(iso).timestamp()
        os.utime(os.path.join(self.tmp, f"work/worklogs/2026-11-07-reuniao-mcp-remoto-{slug}.md"), (ts, ts))

    def estado(self, **kw):
        base = dict(measurements=os.path.join(FIX, "measurements-mini.jsonl"),
                    sessions=os.path.join(FIX, "sessions-mini.jsonl"), codex_dir=os.path.join(FIX, "codex"),
                    opened="2026-11-07T21:28:13-03:00", closed="2026-11-07T21:30:48-03:00",
                    at="2026-11-07T21:32:40-03:00")
        base.update(kw)
        e = tally.build_estado(self.reuniao, 3, self.tmp, **base)
        return {p["nome"]: p for p in e["personas"]}, e

    def test_claude_soma_na_janela(self):
        ps, e = self.estado()
        m = ps["Muralha"]
        self.assertEqual((m["custo_usd"], m["latencia_s"], m["latencia_fonte"], m["janela"]), (0.22, 41, "turno", True))
        self.assertEqual((m["estado"], m["respondeu_as"]), ("respondeu", "21:29:00"))
        self.assertEqual((e["rodada"]["aberta"], e["rodada"]["fechada"], e["rodada"]["gerado"]),
                         ("21:28:13", "21:30:48", "21:32:40"))

    def test_claude_sem_janela_devolve_o_total(self):
        ps, _ = self.estado(opened=None, closed=None)
        m = ps["Muralha"]
        self.assertEqual((m["custo_usd"], m["janela"]), (10.21, False))

    def test_sem_janela_avisa_e_rotula_total_da_sessao(self):
        """B1: sem `--closed` o custo dos Claude é o da sessão inteira e NÃO se rotula 'da rodada'."""
        ps, e = self.estado(closed=None)
        self.assertEqual(e["rodada"]["custo_rotulo"], "total da sessão")
        self.assertFalse(ps["Muralha"]["janela"])
        self.assertTrue(any("TOTAL DA SESSÃO" in a for a in e["avisos"]))
        self.assertIn("total da sessão", tally.render_md(e))
        _, e2 = self.estado()
        self.assertEqual(e2["rodada"]["custo_rotulo"], "da rodada")
        self.assertFalse(any("TOTAL DA SESSÃO" in a for a in e2["avisos"]))

    def test_cli_sem_janela_avisa_em_stderr(self):
        manifesto = os.path.join(self.tmp, "reuniao.json")
        with open(manifesto, "w") as f:
            json.dump(self.reuniao, f)
        err = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            tally.main(["3", "--reuniao", manifesto, "--root", self.tmp, "--out", "-",
                        "--measurements", os.path.join(FIX, "measurements-mini.jsonl"),
                        "--sessions", os.path.join(FIX, "sessions-mini.jsonl"),
                        "--codex-dir", os.path.join(FIX, "codex")])
        self.assertIn("TOTAL DA SESSÃO", err.getvalue())

    def test_persona_sem_ids_no_mapa_diz_sem_medicao_e_o_manifesto_sobrescreve(self):
        """B2b: sem claude_session/provider_session o tally diz por quê, em vez de None mudo."""
        self.reuniao["personas"][0]["sessao"] = "so-no-worker-start"
        ps, e = self.estado()
        self.assertIsNone(ps["Muralha"]["custo_usd"])
        self.assertEqual(ps["Muralha"]["medicao_aviso"], "sem medição: persona sem claude_session/provider_session no mapa")
        self.assertIn("Muralha: sem medição: persona sem claude_session/provider_session no mapa", tally.render_md(e))
        self.reuniao["personas"][0]["claude_session"] = "claude-aaa"   # a sobrescrita do manifesto
        ps, _ = self.estado()
        self.assertEqual((ps["Muralha"]["custo_usd"], ps["Muralha"]["medicao_aviso"]), (0.22, None))
        self.reuniao["personas"][1]["provider_session"] = "prov-regua"
        self.reuniao["personas"][1]["sessao"] = "so-no-worker-start"
        ps, _ = self.estado()
        self.assertEqual(ps["Régua"]["latencia_s"], 155)

    def test_virada_da_meia_noite(self):
        """M1: aberta 23:58 e fechada 00:05 (HH:MM:SS sem data) é uma janela de 7 min, não invertida."""
        mm = os.path.join(self.tmp, "m.jsonl")
        with open(mm, "w") as f:
            f.write(json.dumps({"event": "turn", "session_id": "claude-aaa", "timestamp": "2026-11-08T00:01:00-03:00",
                                "duration_s": 30, "estimated_cost_usd": 0.5}) + "\n")
        self.reuniao["data"] = "2026-11-07"
        ps, e = self.estado(measurements=mm, opened="23:58:00", closed="00:05:00", at="00:06:00")
        self.assertEqual((ps["Muralha"]["custo_usd"], ps["Muralha"]["latencia_s"]), (0.5, 30))
        self.assertEqual((e["rodada"]["aberta"], e["rodada"]["fechada"], e["rodada"]["gerado"]),
                         ("23:58:00", "00:05:00", "00:06:00"))

    def test_marcador_de_rodada_adiante_sem_a_secao_e_sem_dado(self):
        """M2: R2 + marcador 2, depois R4 + marcador 4: para N=3 não há dado, e não é 'respondeu' com None."""
        txt = ("## O que se fez\n\n### Rodada 2: x\n\ntexto\n\n<!-- fim-rodada-2 -->\n\n"
               "### Rodada 4: y\n\ntexto\n\n<!-- fim-rodada-4 -->\n")
        with open(os.path.join(self.tmp, "work/worklogs/2026-11-07-reuniao-mcp-remoto-salto.md"), "w") as f:
            f.write(txt)
        ps, e = self.estado()
        self.assertEqual((ps["Salto"]["estado"], ps["Salto"]["respondeu_as"], ps["Salto"]["confianca"]),
                         ("sem dado", None, None))
        self.assertIn("— (sem dado)", tally.render_md(e))

    def test_virada_antes_vem_da_rodada_anterior(self):
        """M6: `virada_antes` repete a virada da rodada N-1 como etiqueta."""
        txt = ("### Rodada 2: debate\n\n#### Placar da rodada 2\n\n| Assunto | Mudou? | Confiança |\n| :-- | :-- | :-- |\n"
               "| a | virou | 60 |\n\n<!-- fim-rodada-2 -->\n\n### Rodada 3: voto\n\n"
               "| Parte | Confiança | Porquê |\n| :-- | :-- | :-- |\n| **O plano inteiro** | 70 | ok |\n\n<!-- fim-rodada-3 -->\n")
        with open(os.path.join(self.tmp, "work/worklogs/2026-11-07-reuniao-mcp-remoto-salto.md"), "w") as f:
            f.write(txt)
        ps, _ = self.estado()
        self.assertEqual(ps["Salto"]["virada_antes"], "R2: virou")
        self.assertIsNone(ps["Muralha"]["virada_antes"])

    def test_claude_sem_medicao(self):
        ps, _ = self.estado()
        p = ps["Plantão"]  # a sessão claude-bbb não tem evento no measurements
        self.assertIsNone(p["custo_usd"])
        self.assertEqual((p["latencia_s"], p["latencia_fonte"]), (77, "≈ mtime"))
        self.assertEqual(p["estado"], "respondeu")

    def test_codex_latencia_e_tokens_pela_diferenca_com_info_null(self):
        ps, _ = self.estado()
        r = ps["Régua"]
        self.assertEqual((r["latencia_s"], r["latencia_fonte"]), (155, "turno"))
        self.assertEqual(r["tokens"], {"entrada": 600, "cache": 550, "saida": 50})
        self.assertIsNone(r["custo_usd"])
        self.assertEqual(r["respondeu_as"], "21:30:48")

    def test_codex_erro_de_limite_vira_sem_cota(self):
        ps, _ = self.estado()
        self.assertEqual(ps["Atalho"]["estado"], "sem cota")
        self.assertEqual(ps["Atalho"]["latencia_s"], 47)

    def test_codex_sem_janela_nao_escolhe_turno_por_posicao(self):
        """C10: sem janela o turno N-1 por posição erra com um turno a mais; fica None, com o aviso da janela."""
        for n in (2, 3):
            e = tally.build_estado(self.reuniao, n, self.tmp,
                                   measurements=os.path.join(FIX, "measurements-mini.jsonl"),
                                   sessions=os.path.join(FIX, "sessions-mini.jsonl"),
                                   codex_dir=os.path.join(FIX, "codex"))
            r = [p for p in e["personas"] if p["nome"] == "Régua"][0]
            self.assertEqual((r["latencia_s"], r["tokens"]), (None, None), n)
            self.assertTrue(any("sem a janela" in a for a in e["avisos"]))

    def test_codex_com_janela_acha_o_turno_pela_hora(self):
        ps, _ = self.estado(opened="2026-11-07T21:18:00-03:00", closed="2026-11-07T21:20:30-03:00")
        self.assertEqual(ps["Régua"]["latencia_s"], 94)  # o 1º turno do rollout, achado pela janela

    def test_grok_e_antigravity_sem_medicao(self):
        ps, _ = self.estado()
        s = ps["Salto"]
        self.assertEqual((s["custo_usd"], s["tokens"]), (None, None))
        self.assertEqual((s["latencia_s"], s["latencia_fonte"]), (47, "≈ mtime"))
        c = ps["Cartógrafo"]  # sem worklog
        self.assertEqual((c["estado"], c["custo_usd"], c["latencia_s"], c["confianca"], c["linha"]),
                         ("falta", None, None, None, None))

    def test_sala_sem_o_antigravity_e_revisor(self):
        with open(os.path.join(self.tmp, "sintese-3.json"), "w") as f:
            json.dump({"revisor": 45, "revisor_nota": "revisor independente"}, f)
        self.reuniao["dir"] = "."
        _, e = self.estado()
        s = e["sala"]
        self.assertEqual((s["media"], s["n"], s["total"], s["revisor"], s["diferenca_revisor"]), (57.8, 4, 6, 45, 12.8))
        self.assertEqual(s["faixa"], [50.0, 68.0])

    def test_revisor_aninhado_em_sala_e_solto_e_a_diferenca(self):
        """C6: o molde do `sintese-N.json` põe o revisor em `sala`; o tally lê os dois jeitos."""
        self.reuniao["dir"] = "."
        for conteudo in ({"sala": {"revisor": 45, "revisor_nota": "independente"}},
                         {"revisor": 45, "revisor_nota": "independente"}):
            with open(os.path.join(self.tmp, "sintese-3.json"), "w") as f:
                json.dump(conteudo, f)
            _, e = self.estado()
            self.assertEqual((e["sala"]["revisor"], e["sala"]["revisor_nota"], e["sala"]["diferenca_revisor"]),
                             (45, "independente", 12.8))
            self.assertIn("revisor 45", tally.render_md(e))
            self.assertIn("sala − revisor +12,8", tally.render_md(e))

    def test_media_da_sala_so_de_quem_respondeu(self):
        """C7: quem está `falta` não entra na média nem no n (caso 57 (3/6) × 52,5 (2/6) do relatório)."""
        ps = [{"nome": n, "runtime": "Claude", "estado": est, "confianca": c} for n, est, c in
              [("A", "respondeu", 40), ("B", "respondeu", 65), ("C", "falta", 66), ("D", "respondeu", None)]]
        s = tally.calc_sala(ps)
        self.assertEqual((s["media"], s["n"], s["mediana"], s["total"]), (52.5, 2, 52.5, 4))

    def test_render_md(self):
        ps, e = self.estado()
        md = tally.render_md(e)
        self.assertIn("| Persona | Posição em uma linha | Confiança | Mudou? | Voto |", md)
        self.assertIn("| Muralha | porque 58 | 58 | — | — |", md)  # sem R1 no worklog: sem delta
        self.assertIn("— (falta)", md)
        self.assertIn("Sala: média 57,8 (4/6), mediana 56,5, faixa 50–68", md)
        self.assertIn("Sem medição de custo: Salto (Grok), Cartógrafo (Antigravity).", md)

    def test_cli_grava_o_estado_e_imprime_a_tabela(self):
        manifesto = os.path.join(self.tmp, "reuniao.json")
        self.reuniao["dir"] = ".sessions/x"
        with open(manifesto, "w") as f:
            json.dump(self.reuniao, f)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = tally.main(["3", "--reuniao", manifesto, "--root", self.tmp,
                             "--opened", "21:28:13", "--closed", "21:30:48",
                             "--measurements", os.path.join(FIX, "measurements-mini.jsonl"),
                             "--sessions", os.path.join(FIX, "sessions-mini.jsonl"),
                             "--codex-dir", os.path.join(FIX, "codex")])
        self.assertEqual(rc, 0)
        self.assertIn("Sala: média", buf.getvalue())
        with open(os.path.join(self.tmp, ".sessions/x/estado-r3.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["rodada"]["n"], 3)


class ParserTolerante(unittest.TestCase):
    """C11: variação razoável de worklog lê certo; o que é dúvida vira None e aviso, nunca número inventado."""

    def rodada(self, txt, n, names=()):
        return tally.parse_worklog(txt, names)["rodadas"][n]

    def test_titulo_de_secao_com_travessao_ou_dois_hashes(self):
        for h in ("### Rodada 3 — a confiança", "## Rodada 3: a confiança", "### Rodada 3 - a confiança", "### Rodada 3: a confiança"):
            r = self.rodada(h + "\n\n| Parte | Confiança |\n| :-- | :-- |\n| **O plano inteiro** | 68 |\n", 3)
            self.assertEqual((r["confianca"], r["titulo"]), (68.0, "a confiança"), h)

    def test_formas_do_numero(self):
        for cel in ("**68**/100", "68%", "**68/100**", " 68 / 100 ", "68,0"):
            self.assertEqual(tally.to_num(cel), 68.0, cel)
        self.assertEqual(tally.to_num("**8**/10"), 8.0)
        for cel in ("3 vezes", "R2", "abc", ""):
            self.assertIsNone(tally.to_num(cel), cel)

    def test_o_plano_inteiro_com_sufixo(self):
        for rot in ("**O plano inteiro (v2)**", "O plano inteiro", "o plano inteiro — v3"):
            r = self.rodada(f"### Rodada 4: x\n\n| Parte | v1 | v2 |\n| :-- | :-- | :-- |\n| {rot} | 58 | **72** |\n", 4)
            self.assertEqual(r["confianca"], 72.0, rot)

    def test_colegas_com_colunas_trocadas_acha_pelo_cabecalho(self):
        t = ("### Rodada 3: x\n\n#### Os colegas\n\n| Nota de 0 a 10 | A contribuição | Persona |\n| :-- | :-- | :-- |\n"
             "| 9 | os fatos | Faísca |\n| 7 | o piloto | Cinza |\n")
        self.assertEqual(self.rodada(t, 3)["notas"], {"Faísca": 9.0, "Cinza": 7.0})

    def test_colegas_sem_coluna_de_nota_avisa(self):
        t = "### Rodada 3: x\n\n#### Os colegas\n\n| Persona | Contribuição |\n| :-- | :-- |\n| Faísca | 9 |\n"
        r = self.rodada(t, 3)
        self.assertIsNone(r["notas"])
        self.assertTrue(r["avisos"])

    def test_prosa_com_numero_que_nao_e_nota_nao_vira_nota(self):
        t = "### Rodada 3: x\n\n- **Nota aos colegas:** Régua 9/10, citou Muralha 3 vezes\n\n"
        r = self.rodada(t, 3, ["Régua", "Muralha"])
        self.assertEqual(r["notas"], {"Régua": 9.0})
        self.assertTrue(any("Muralha" in a for a in r["avisos"]))
        t2 = "### Rodada 3: x\n\n- **Nota aos colegas:** Muralha (R2) 9\n\n"
        self.assertIsNone(self.rodada(t2, 3, ["Muralha"])["notas"])

    def test_prosa_aceita_n_barra_10_e_numero_solto_com_pontuacao(self):
        t = ("### Rodada 3: x\n\n- **Nota aos colegas:**\n  - Régua 9 / 10 — a\n  - Muralha: 9. b\n"
             "  - Salto 8 / 10 c\n  - **Atalho (10/10):** d\n\n")
        self.assertEqual(self.rodada(t, 3, ["Régua", "Muralha", "Salto", "Atalho"])["notas"],
                         {"Régua": 9.0, "Muralha": 9.0, "Salto": 8.0, "Atalho": 10.0})

    def test_confianca_linha_em_negrito(self):
        r = self.rodada("### Rodada 5: x\n\n**Confiança:** **74**/100\n", 5)
        self.assertEqual((r["confianca"], r["confianca_fonte"]), (74.0, "confianca-linha"))


class RaizPadrao(unittest.TestCase):
    """C8: o resultado é o mesmo rodando da raiz do worktree, da pasta da reunião ou da pasta da skill."""

    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        subprocess.run(["git", "init", "-q", self.tmp], check=True)
        reu = load("reuniao-mcp-remoto.json")
        reu["dir"] = ".sessions/x"
        reu["personas"] = reu["personas"][:2]
        self.reu = reu
        os.makedirs(os.path.join(self.tmp, ".sessions/x"))
        os.makedirs(os.path.join(self.tmp, ".claude/skills/meeting-runner"))
        with open(os.path.join(self.tmp, ".sessions/x/reuniao.json"), "w", encoding="utf-8") as f:
            json.dump(reu, f)
        os.makedirs(os.path.join(self.tmp, "work/worklogs"))

    def worklog(self, slug, conf):
        with open(os.path.join(self.tmp, f"work/worklogs/2026-11-07-reuniao-mcp-remoto-{slug}.md"), "w", encoding="utf-8") as f:
            f.write(f"### Rodada 3: x\n\n| Parte | Confiança | Porquê |\n| :-- | :-- | :-- |\n"
                    f"| **O plano inteiro** | {conf} | ok |\n\n<!-- fim-rodada-3 -->\n")

    def roda(self, cwd, reuniao):
        r = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(HERE), "tally.py"), "3", "--reuniao", reuniao,
                            "--json", "--opened", "21:28:13", "--closed", "21:30:48",
                            "--measurements", os.path.join(FIX, "inexistente"), "--sessions", os.path.join(FIX, "inexistente"),
                            "--codex-dir", os.path.join(FIX, "inexistente")],
                           cwd=os.path.join(self.tmp, cwd), capture_output=True, text=True)
        return r

    def test_o_mesmo_resultado_de_tres_diretorios(self):
        self.worklog("muralha", 58)
        self.worklog("regua", 68)
        vistos = []
        for cwd, reu in ((".", ".sessions/x/reuniao.json"), (".sessions/x", "reuniao.json"),
                         (".claude/skills/meeting-runner", ".sessions/x/reuniao.json")):
            r = self.roda(cwd, reu)
            self.assertEqual(r.returncode, 0, (cwd, r.stderr))
            e = json.loads(r.stdout)
            vistos.append(([(p["nome"], p["estado"], p["confianca"]) for p in e["personas"]], e["sala"]["media"]))
            # o estado vai para <raiz>/<dir>, nunca para <cwd>/<dir>
            self.assertTrue(os.path.isfile(os.path.join(self.tmp, ".sessions/x/estado-r3.json")))
            self.assertFalse(os.path.exists(os.path.join(self.tmp, ".sessions/x/.sessions")))
        self.assertEqual(vistos[0], vistos[1])
        self.assertEqual(vistos[0], vistos[2])
        self.assertEqual(vistos[0][0], [("Muralha", "respondeu", 58.0), ("Régua", "respondeu", 68.0)])

    def test_sem_nenhum_worklog_e_erro_explicito(self):
        for cwd, reu in ((".", ".sessions/x/reuniao.json"), (".sessions/x", "reuniao.json")):
            r = self.roda(cwd, reu)
            self.assertEqual(r.returncode, 2, cwd)
            self.assertIn("nenhum worklog existe", r.stderr)
            self.assertNotIn("falta", r.stdout)

    def test_raiz_padrao_cai_para_o_cwd_fora_do_git(self):
        fora = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, fora, True)
        antes = os.getcwd()
        os.chdir(fora)
        try:
            self.assertEqual(os.path.realpath(tally.raiz_padrao()), os.path.realpath(fora))
        finally:
            os.chdir(antes)


class AceiteComMedicaoReal(unittest.TestCase):
    """C15: latência e custo contra o gabarito de `levantamento-processo.md` 3.1 e 3.2, com a medição e os rollouts reais.
    Falta de dado (arquivo ausente) é skip; erro do tally é falha."""

    @classmethod
    def setUpClass(cls):
        cls.root = raiz_do_repo()
        cls.meas = tally.default_file(cls.root, ".measurements/measurements.jsonl")
        cls.sess = tally.default_file(cls.root, ".sessions/sessions.jsonl")
        cls.codex = os.path.expanduser("~/.codex/sessions")
        if not (os.path.isfile(cls.meas) and os.path.isfile(cls.sess) and os.path.isdir(cls.codex)
                and os.path.isfile(os.path.join(cls.root, "work/worklogs/2026-11-07-reuniao-mcp-remoto-muralha.md"))):
            raise unittest.SkipTest("sem as medições e os rollouts reais de 2026-11-07 neste computador")
        cls.mcp, cls.carvao = load("reuniao-mcp-remoto.json"), load("reuniao-carvao.json")

    def estado(self, reuniao, n, abre, fecha):
        e = tally.build_estado(reuniao, n, self.root, measurements=self.meas, sessions=self.sess, codex_dir=self.codex,
                               opened=abre, closed=fecha)
        return {p["nome"]: p for p in e["personas"]}

    def test_r3_da_mcp(self):  # 3.2: Muralha 41 s, Régua 155 s, Atalho 35 s, Plantão 24 s
        ps = self.estado(self.mcp, 3, "21:28:13", "21:30:48")
        self.assertEqual((ps["Muralha"]["custo_usd"], ps["Muralha"]["latencia_s"]), (0.22, 41))
        self.assertEqual((ps["Plantão"]["latencia_s"], ps["Plantão"]["custo_usd"]), (24, 0.03))
        self.assertEqual(ps["Régua"]["latencia_s"], 155)
        self.assertEqual(ps["Régua"]["tokens"]["entrada"], 661376)
        self.assertEqual(ps["Atalho"]["latencia_s"], 35)

    def test_r7_de_carvao_acha_o_turno_pela_janela_e_nao_o_da_r6b(self):  # 3.1: R7 = 27, 24, 20, 21 s
        ps = self.estado(self.carvao, 7, "20:35:00", "20:35:30")
        self.assertEqual((ps["Cinza"]["latencia_s"], ps["Lenha"]["latencia_s"]), (24, 20))  # a R6b deu 25 e 23
        self.assertEqual((ps["Tição"]["latencia_s"], ps["Fole"]["latencia_s"]), (27, 21))

    def test_custo_total_de_carvao(self):  # 3.1: Tição US$ 3,61 (8 turnos), Fole US$ 3,13
        ps = self.estado(self.carvao, 7, "19:59:00", "20:36:00")
        self.assertEqual((ps["Tição"]["custo_usd"], ps["Fole"]["custo_usd"]), (3.61, 3.13))

    def test_codex_sem_janela_nao_chuta(self):
        e = tally.build_estado(self.carvao, 7, self.root, measurements=self.meas, sessions=self.sess, codex_dir=self.codex)
        ps = {p["nome"]: p for p in e["personas"]}
        self.assertIsNone(ps["Cinza"]["latencia_s"])


class FormaDoEstado(unittest.TestCase):
    def test_mesmas_chaves_do_estado_r3(self):
        ref = load("estado-r3.json")
        e = tally.build_estado(load("reuniao-mcp-remoto.json"), 3, os.path.join(FIX, "inexistente"),
                               measurements="x", sessions="x", codex_dir="x")
        for k in ("reuniao", "rodada", "sala", "custos_coordenacao", "medicoes", "sintese", "decisoes"):
            self.assertIn(k, e)
        self.assertEqual(set(ref["rodada"]) - set(e["rodada"]), set())
        faltam = set(ref["personas"][0]) - set(e["personas"][0])
        self.assertEqual(faltam, set())
        self.assertTrue(all(p["estado"] == "falta" for p in e["personas"]))  # sem worklog: falta, sem exceção


if __name__ == "__main__":
    unittest.main()
