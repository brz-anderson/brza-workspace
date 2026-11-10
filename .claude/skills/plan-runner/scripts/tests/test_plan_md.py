import os
import shutil
import unittest

import _paths  # noqa: F401
import plan_md
from mini import DESENHO, RODADA1, passo, plano


class Horas(unittest.TestCase):
    def test_ponto_virgula_aproximado_e_vazio(self):
        self.assertEqual(plan_md.parse_horas("11,5 h"), 11.5)
        self.assertEqual(plan_md.parse_horas("11.5 h"), 11.5)
        self.assertEqual(plan_md.parse_horas("~4 h (estimativa de relógio)"), 4.0)
        self.assertEqual(plan_md.parse_horas("0,174 h (janela)"), 0.174)
        self.assertIsNone(plan_md.parse_horas("— h"))
        self.assertIsNone(plan_md.parse_horas(""))
        self.assertIsNone(plan_md.parse_horas("incluído nas 1,109 h agregadas"))

    def test_formato(self):
        self.assertEqual(plan_md.fmt_horas(41.0), "41")
        self.assertEqual(plan_md.fmt_horas(34.75), "34.75")
        self.assertEqual(plan_md.fmt_horas(9.5160000001), "9.516")


class PlanosReais(unittest.TestCase):
    def test_resolve_pln_pela_raiz_e_junta_o_design(self):
        pl = plan_md.carrega("PLN-021", raiz=_paths.RAIZ)
        self.assertEqual(pl.id, "PLN-021")
        self.assertEqual([a.nome for a in pl.arquivos], ["PLN-021-plan.md", "PLN-021-design.md"])
        self.assertTrue(pl.dividido())
        self.assertEqual(pl.fm["phase"], "execution")
        self.assertEqual(pl.fm["scope"], ["workspace"])

    def test_ids_do_pln021(self):
        ids = plan_md.carrega("PLN-021", raiz=_paths.RAIZ).ids()
        self.assertEqual(ids["P"], ["P%d" % i for i in range(1, 11)])
        self.assertEqual(ids["D"], ["D%d" % i for i in range(1, 8)])
        self.assertEqual(ids["X"], ["X1"])
        self.assertEqual(len(ids["R"]), 20)  # R1:4 R2:4 R3:3 R4:9
        self.assertIn("R4.9", ids["R"])
        self.assertIn("D3/A1", ids["A"])

    def test_passos_do_pln021(self):
        pl = plan_md.carrega("PLN-021", raiz=_paths.RAIZ)
        p2 = pl.passo("P2")
        self.assertEqual(p2.executa, ["D6"])
        self.assertEqual(p2.estimado_h, 11.5)
        self.assertIsNone(p2.executado_h)
        self.assertFalse(p2.executado_preenchido)
        self.assertEqual(p2.estado, "pendente")
        self.assertEqual(pl.passo("P3").depende, ["P1", "P2"])
        self.assertEqual(pl.passo("P8").depende, ["P1", "P2", "P3", "P4", "P5", "P6", "P7"])

    def test_pln017_fechado_com_evidencias(self):
        pl = plan_md.carrega("PLN-017", raiz=_paths.RAIZ)
        ids = [p.id for p in pl.passos()]
        self.assertEqual(ids, ["P1", "P2", "P3", "P4a", "P4b", "P5", "P6", "P7", "P8"])
        self.assertTrue(all(p.estado == "feito" for p in pl.passos()))
        self.assertEqual(pl.passo("P1").estimado_h, 10.5)
        self.assertEqual(pl.passo("P1").executado_h, 4.0)
        self.assertIn("bf06d0a", pl.passo("P1").evidencia)
        self.assertIsNone(pl.passo("P4a").executado_h)
        self.assertTrue(pl.passo("P4a").executado_preenchido)
        self.assertEqual(len(pl.rodadas()), 10)
        self.assertEqual(pl.rodada(8).perguntas[0].k, 1)  # a pergunta única de `**Pergunta:**`

    def test_perguntas_decidida_literal_reaberta(self):
        pl = plan_md.carrega("PLN-021", raiz=_paths.RAIZ)
        q = pl.pergunta("R1.2")
        self.assertTrue(q.decidida)
        self.assertEqual(q.reaberta, "R3.1")
        self.assertEqual([o["recomendada"] for o in q.opcoes()], [True, False, False])
        q = pl.pergunta("R2.1")
        self.assertIn("pasta script/ em .claude/", q.resposta)
        self.assertFalse(q.decidida)
        self.assertTrue(pl.rodada(4).sem_resposta)


class Mini(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def monta(self, *a, **k):
        raiz, path = _paths.plano_tmp(*a, **k)
        self.dirs.append(raiz)
        return raiz, path

    def test_heading_em_cerca_nao_conta(self):
        raiz, path = self.monta(plano(passo(), RODADA1), design=DESENHO)
        pl = plan_md.carrega(path)
        self.assertEqual([d["id"] for d in pl.desenhos()], ["D1", "D2"])
        self.assertFalse([s for s in pl.todas_secoes() if "isto não é heading" in s.titulo])

    def test_origem_e_alternativas(self):
        raiz, path = self.monta(plano(passo(), RODADA1), design=DESENHO)
        d = plan_md.carrega(path).desenho("D1")
        self.assertEqual(d["origem_rs"], ["R1.1", "R1.2"])
        self.assertEqual(d["alternativas"], ["A1", "A2"])

    def test_pln_sem_raiz_sobe_ate_plans(self):
        raiz, path = self.monta(plano(passo(), RODADA1))
        pl = plan_md.carrega("PLN-900", raiz=raiz)
        self.assertEqual(os.path.realpath(pl.path), os.path.realpath(path))
        with self.assertRaises(plan_md.PlanoNaoEncontrado):
            plan_md.carrega("PLN-901", raiz=raiz)

    def test_horas_com_ponto_virgula_e_vazio(self):
        raiz, path = self.monta(plano(passo("P1", est="2,5") + passo("P2", est="1.5", exe="— h")))
        ps = plan_md.carrega(path).passos()
        self.assertEqual([p.estimado_h for p in ps], [2.5, 1.5])
        self.assertEqual([p.executado_h for p in ps], [None, None])

    def test_interview_dividido(self):
        raiz, path = self.monta(plano(passo()).replace("## Entrevista\n", ""), interview="# PLN-900 — Entrevista\n\n" + RODADA1.replace("###", "##"))
        pl = plan_md.carrega(path)
        self.assertEqual([a.papel for a in pl.arquivos], ["plan", "interview"])
        self.assertEqual(pl.ids_r(), ["R1.1", "R1.2"])

    def test_perguntas_explicitas(self):
        inter = ("# PLN-900 — Entrevista\n\n## Rodada 2 — o cliente (preparada 2026-11-09, não enviada)\n\n"
                 "**R2.1. Onde mora?**\n\n1. **Módulo (Recomendado).** Custo: um.\n2. **Só o verbo.** Custo: dois.\n\n"
                 "**R2.2. Quanto tempo?**\n\n1. **90 dias.** Custo: x.\n")
        raiz, path = self.monta(plano(passo()).replace("## Entrevista\n", ""), interview=inter)
        self.assertEqual(plan_md.carrega(path).ids_r(), ["R2.1", "R2.2"])


if __name__ == "__main__":
    unittest.main()
