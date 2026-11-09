"""Testes do panel.py sobre o P7 real (R3 da Trava e do Relance, com o Prumo fora): X2, X4, X7, X12, X13, X14, X18."""
import copy
import json
import os
import re
import shutil
import tempfile
import unittest

import _paths  # noqa: F401
from _paths import fixture

import panel
from p7 import monta_raiz


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.root, self.reuniao = monta_raiz(self.tmp)
        self.nada = os.path.join(self.tmp, "nao-existe")

    def collect(self, **kw):
        return panel.collect(self.reuniao, 3, self.root, opened="18:37:02", at="18:38:50", measurements=self.nada,
                             sessions=self.nada, codex_dir=self.nada, **kw)


class X18Subconjunto(Base):
    def test_a_rodada_fecha_quando_todos_os_participantes_responderam(self):
        S = self.collect(participantes=["Trava", "Relance"])
        self.assertIsNotNone(S["rodada"]["fechada"])
        prumo = next(p for p in S["personas"] if p["nome"] == "Prumo")
        self.assertEqual(prumo["estado"], "fora da rodada")
        html = panel.render_html(S)
        self.assertIn("2 de 2 responderam", html)
        self.assertNotIn("3 de 3", html)
        self.assertIn("fora da rodada", html)
        self.assertIn("(1/2)", html)                      # a média da sala é dos participantes (Relance, E-1, à parte)
        # com a rodada fechada, as medições, a síntese e as decisões aparecem (o defeito era ficarem escondidas)
        for t in ("As medições da coordenação", "A síntese", "Para Anderson decidir"):
            self.assertIn(t, html)
        self.assertNotIn("entram quando a rodada fecha", html)
        self.assertNotRegex(html, r"falta[^<]*Prumo")

    def test_sem_o_subconjunto_o_prumo_segura_o_fechamento_e_esconde_os_blocos(self):
        S = self.collect()
        self.assertIsNone(S["rodada"]["fechada"])
        html = panel.render_html(S)
        self.assertNotIn("As medições da coordenação", html)
        self.assertIn("entram quando a rodada fecha", html)

    def test_cli_collect_participantes(self):
        import contextlib
        import io
        manifesto = os.path.join(self.root, ".sessions/reuniao-ci-no-chat/reuniao.json")
        out = os.path.join(self.tmp, "estado.json")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = panel.main(["collect", "3", "--reuniao", manifesto, "--root", self.root, "--measurements", self.nada,
                             "--sessions", self.nada, "--codex-dir", self.nada, "--participantes", "Trava", "Relance",
                             "--out", out])
        self.assertEqual(rc, 0)
        with open(out, encoding="utf-8") as f:
            self.assertEqual(json.load(f)["rodada"]["participantes"], ["Trava", "Relance"])


class Decisoes(Base):
    def test_levantada_por_e_recomendacao_nunca_recomendam(self):
        html = panel.render_html(self.collect(participantes=["Trava", "Relance"]))
        self.assertIn("levantada por Prumo, Trava e Relance", html)
        self.assertIn("recomendação: A (3/3)", html)
        self.assertNotRegex(html, r"recomendam?:")

    def test_um_levantador_e_voto_so_do_campo_votos(self):
        S = self.collect(participantes=["Trava", "Relance"])
        S["decisoes"] = [{"pergunta": "P?", "quem": ["Prumo"], "recomendacao": "A", "votos": None},
                         {"pergunta": "Q?", "quem": ["Trava"], "recomendacao": "B", "votos": "2 A, 1 B"}]
        html = panel.render_html(S)
        self.assertIn("levantada por Prumo", html)
        self.assertEqual(html.count("2 A, 1 B"), 1)
        primeira = html.split("<b>P?</b>")[1].split("</li>")[0]
        self.assertNotIn("A, 1 B", primeira)
        self.assertNotIn("votos", primeira)


class Cartao(unittest.TestCase):
    def estado(self):
        with open(fixture("estado-r3.json"), encoding="utf-8") as f:
            return json.load(f)

    def test_o_cartao_so_fala_do_codex_quando_ha_persona_codex(self):
        S = self.estado()
        self.assertIn("Codex", panel.render_html(S))                # a MCP tem Régua e Atalho em Codex
        for p in S["personas"]:
            if str(p["runtime"]).lower() == "codex":
                p["runtime"] = "Claude"
        html = panel.render_html(S)
        self.assertNotIn("Codex", html)
        self.assertIn("personas Claude na rodada", html)

    def test_cabecalho_do_custo_leva_o_rotulo_do_total(self):
        S = self.estado()
        self.assertIn('<div class="ct">Custo</div>', panel.render_html(S))
        S["rodada"]["custo_rotulo"] = "total da sessão"
        html = panel.render_html(S)
        self.assertIn('<div class="ct">Custo (total da sessão)</div>', html)
        self.assertIn("no total da sessão", html)

    def test_pendente_mostra_medicao_pendente_e_nao_sem_medicao(self):
        S = self.estado()
        p = next(x for x in S["personas"] if x["runtime"] == "Claude")
        p.update(medicao="pendente", custo_usd=None, tokens=None)
        html = panel.render_html(S)
        self.assertIn("medição pendente", html)
        self.assertIn("Medição pendente: " + p["nome"], html)
        sem = re.search(r"Sem medição: ([^.]*)\.", html).group(1)
        self.assertNotIn(p["nome"], sem)      # a pendente não é "sem medição"


class Virada(unittest.TestCase):
    def tags(self, virada):
        p = {"nome": "X", "estado": "respondeu", "virada": virada}
        return panel._tags(p, False)

    def test_a_etiqueta_e_a_propria_palavra(self):
        for v in ("virou", "ajustou"):
            t = self.tags(v)
            self.assertIn(f">{v}<", t)
            self.assertNotIn("virou: virou", t)
            self.assertNotIn(f"{v}: {v}", t)
        self.assertIn(">manteve<", self.tags("não"))
        self.assertNotIn(">não<", self.tags("não"))


class Paralelo(Base):
    def test_o_html_troca_o_sinal_de_paralelo_e_o_json_fica(self):
        S = self.collect(participantes=["Trava", "Relance"])
        S["personas"][1]["posicao"] = "Sync ∥ sombra; disparo real só após o critério"
        antes = json.dumps(S, ensure_ascii=False)
        html = panel.render_html(S)
        self.assertIn("Sync || sombra", html)
        self.assertNotIn("∥", html)
        self.assertEqual(json.dumps(S, ensure_ascii=False), antes)   # o render não muta o estado
        self.assertIn("∥", antes)

    def test_escape_html_continua(self):
        self.assertEqual(panel._e("<b>&</b>"), "&lt;b&gt;&amp;&lt;/b&gt;")
        self.assertEqual(panel._e(None), "")


class CabecalhoComum(unittest.TestCase):
    def test_o_painel_e_a_espera_leem_a_mesma_duracao(self):
        import common
        import wait_round
        self.assertIs(panel._cabecalho_rodada, common.cabecalho_rodada)
        t, prazo, dur = panel._cabecalho_rodada(fixture("p7", "rodada-3.md"))
        self.assertEqual((t, prazo, dur), ("o voto informado entre A e B", None, 5))
        self.assertIs(wait_round.common, common)


class VotoNoPainel(Base):
    def test_palavras_inteiras_e_voto_por_proposta(self):
        html = panel.render_html(self.collect(participantes=["Trava", "Relance"]))
        self.assertIn("voto A: apoio c/ ressalva · B: contra", html)
        self.assertNotRegex(html, r"voto A \d")

    def test_sem_voto_por_proposta_cai_para_as_contagens_em_palavras(self):
        S = self.collect(participantes=["Trava", "Relance"])
        for p in S["personas"]:
            p.pop("voto_por_proposta", None)
        html = panel.render_html(S)
        self.assertIn("voto: apoio 0 · ressalva 1 · contra 1", html)

    def test_participantes_desconhecido_sai_2(self):
        import contextlib, io
        manifesto = os.path.join(self.root, ".sessions/reuniao-ci-no-chat/reuniao.json")
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            rc = panel.main(["collect", "3", "--reuniao", manifesto, "--root", self.root, "--measurements", self.nada,
                             "--sessions", self.nada, "--codex-dir", self.nada, "--participantes", "Fulano",
                             "--out", os.path.join(self.tmp, "e.json")])
        self.assertEqual(rc, 2)
        self.assertIn("persona desconhecida: Fulano", err.getvalue())

    def test_participantes_em_minusculo_resolvem(self):
        S = self.collect(participantes=["trava", "relance"])
        self.assertEqual(S["rodada"]["participantes"], ["Trava", "Relance"])


class CartaoSemClaude(Base):
    def test_sem_claude_entre_os_participantes_nao_mostra_us_0(self):
        html = panel.render_html(self.collect(participantes=["Trava", "Relance"]))
        self.assertIn("sem persona Claude na rodada", html)
        self.assertNotIn("US$ 0,00</b><span>personas Claude", html)
        self.assertNotIn("personas Claude na rodada", html)


class CodexForaDaRodada(unittest.TestCase):
    """A4 (X2): o cartão falava do Codex quando a persona Codex estava fora da rodada."""

    def test_codex_fora_da_rodada_nao_aparece_no_cartao(self):
        with open(fixture("estado-r3.json"), encoding="utf-8") as f:
            S = json.load(f)
        nomes = [p["nome"] for p in S["personas"] if str(p["runtime"]).lower() != "codex"]
        for p in S["personas"]:
            if str(p["runtime"]).lower() == "codex":
                p["estado"] = "fora da rodada"
        S["rodada"]["participantes"] = nomes
        html = panel.render_html(S)
        self.assertNotIn("Codex 0", html)
        self.assertNotIn("M tokens", html)


class CabecalhoSemClaude(Base):
    """A4 no painel: o cabeçalho "Custo (total da sessão)" só cabe com algum Claude entre os participantes."""

    def test_sem_claude_na_rodada_o_cabecalho_nao_fala_do_total(self):
        S = self.collect(participantes=["Trava", "Relance"])
        self.assertEqual(S["rodada"]["custo_rotulo"], "total da sessão")
        self.assertNotIn("Custo (total da sessão)", panel.render_html(S))

    def test_com_o_prumo_na_rodada_o_cabecalho_continua(self):
        self.assertIn("Custo (total da sessão)", panel.render_html(self.collect()))


if __name__ == "__main__":
    unittest.main()
