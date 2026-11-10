import io
import json
import os
import shutil
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import plan_md
import plan_state
from mini import DESENHO, RODADA1, passo, plano

EV = "`brza-workspace@a1b2c3d` · `python3 -m unittest` → 12 OK"


def codigos(est, nivel=None):
    return sorted(p["codigo"] for p in est["problemas"] if nivel is None or p["nivel"] == nivel)


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def monta(self, *a, **k):
        raiz, path = _paths.plano_tmp(*a, **k)
        self.dirs.append(raiz)
        return raiz, path

    def estado(self, *a, **k):
        raiz, path = self.monta(*a, **k)
        return plan_state.estado(path)

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = plan_state.main(list(args) + ["--no-panel"])
        return rc, out.getvalue(), err.getvalue()


class PlanosReais(Base):
    def test_pln021_aberto_limpo(self):
        est = plan_state.estado("PLN-021", raiz=_paths.RAIZ)
        self.assertEqual(est["problemas"], [])
        self.assertEqual(est["proximo"], "P1")
        self.assertEqual(est["horas"]["somado"]["estimate_h"], 41)
        self.assertTrue(est["horas"]["confere"])
        self.assertEqual(est["ids"]["P"][-1], "P10")
        self.assertEqual([p["estado"] for p in est["passos"]], ["pendente"] * 10)
        self.assertEqual(est["passos"][1]["executa"], ["D6"])

    def test_pln017_fechado_acha_a_evidencia_e_as_horas(self):
        est = plan_state.estado("PLN-017", raiz=_paths.RAIZ)
        erros = [(p["codigo"], p["onde"]) for p in est["problemas"] if p["nivel"] == "erro"]
        self.assertIn(("checked-without-evidence", "P7"), erros)
        self.assertIn(("hours-mismatch", "frontmatter:executed_h"), erros)
        self.assertEqual(len(erros), 2)
        self.assertIsNone(est["proximo"])
        self.assertFalse(est["horas"]["confere"])
        self.assertEqual(est["horas"]["frontmatter"]["executed_h"], 9.516)
        self.assertEqual(est["horas"]["somado"]["estimate_h"], 34.75)
        self.assertTrue(all(p["estado"] == "feito" for p in est["passos"]))
        # a P7 é a única `[x]` sem evidência válida
        self.assertEqual([p["id"] for p in est["passos"] if not p["evidencia"]], ["P7"])

    def test_cli_exit_codes_nos_reais(self):
        pln21 = os.path.join(_paths.RAIZ, "plans", "PLN-021-o-plano-coordenado-e-os-artboards", "PLN-021-plan.md")
        pln17 = os.path.join(_paths.RAIZ, "plans", "PLN-017-a-reuniao-multiagente-como-fluxo-replicavel", "PLN-017-plan.md")
        self.assertEqual(self.cli(pln21)[0], 0)
        self.assertEqual(self.cli(pln17)[0], 1)
        rc, out, _ = self.cli(pln21, "--json")
        self.assertEqual(json.loads(out)["proximo"], "P1")
        rc, out, _ = self.cli(pln21, "--next")
        self.assertEqual((rc, out.split(" —")[0]), (0, "P1"))
        self.assertEqual(self.cli("PLN-999-que-nao-existe")[0], 2)
        self.assertEqual(self.cli()[0], 2)


class Codigos(Base):
    def test_limpo(self):
        est = self.estado(plano(passo("P1", est="5") , RODADA1), design=DESENHO)
        self.assertEqual(est["problemas"], [])

    def test_checked_without_evidence_sem_evidencia(self):
        est = self.estado(plano(passo(checks="- [x] **1. A**", exe="1 h", est="5"), RODADA1, rest="0", exe="1"), design=DESENHO)
        self.assertIn("checked-without-evidence", codigos(est))

    def test_checked_without_evidence_evidencia_vazia_de_prova(self):
        est = self.estado(plano(passo(checks="- [x] **1. A**", exe="1 h", est="5",
                                      evidencia="feito, confia"), RODADA1, rest="0", exe="1"), design=DESENHO)
        self.assertIn("checked-without-evidence", codigos(est))

    def test_evidencia_com_commit_comando_ou_arquivo_linha_vale(self):
        for ev in ("`brza-workspace@bf06d0a`", "`pytest` → 3 OK", "`scripts/x.py:42` muda o que o D pede"):
            est = self.estado(plano(passo(checks="- [x] **1. A**", exe="1 h", est="5", evidencia=ev), RODADA1,
                                    rest="0", exe="1"), design=DESENHO)
            self.assertNotIn("checked-without-evidence", codigos(est), ev)

    def test_id_com_underscore_nao_e_commit(self):
        est = self.estado(plano(passo(checks="- [x] **1. A**", exe="1 h", est="5", evidencia="o run run_fe70b351bc36 rodou"),
                                RODADA1, rest="0", exe="1"), design=DESENHO)
        self.assertIn("checked-without-evidence", codigos(est))

    def test_checked_without_executed(self):
        est = self.estado(plano(passo(checks="- [x] **1. A**", exe="— h", est="5", evidencia=EV), RODADA1, rest="0", exe="0"),
                          design=DESENHO)
        self.assertEqual(codigos(est), ["checked-without-executed"])

    def test_executado_em_texto_conta_como_preenchido(self):
        est = self.estado(plano(passo(checks="- [x] **1. A**", exe="incluído nas 1,1 h agregadas", est="5", evidencia=EV),
                                RODADA1, rest="0", exe="0"), design=DESENHO)
        self.assertNotIn("checked-without-executed", codigos(est))

    def test_hours_mismatch(self):
        est = self.estado(plano(passo(est="5"), RODADA1, est="9", exe="0", rest="5"), design=DESENHO)
        self.assertEqual(codigos(est), ["hours-mismatch"])
        self.assertFalse(est["horas"]["confere"])
        self.assertEqual(est["horas"]["somado"], {"estimate_h": 5.0, "executed_h": 0.0, "remaining_h": 5.0})

    def test_descartado_sai_das_somas(self):
        passos = passo("P1", est="2", exe="1 h", checks="- [x] **1. A**", evidencia=EV) + \
            passo("P2", executa="Executa D2", est="3", checks="- [-] **1. A** — descartado porque o D mudou") + \
            passo("P3", executa="Executa D2", est="4")
        est = self.estado(plano(passos, RODADA1, est="6", exe="1", rest="4"), design=DESENHO)
        self.assertEqual(est["problemas"], [])
        self.assertEqual([p["estado"] for p in est["passos"]], ["feito", "descartado", "pendente"])
        self.assertEqual(est["proximo"], "P3")

    def test_step_without_design(self):
        est = self.estado(plano(passo("P1", executa="Executor: a sessão"), RODADA1), design=DESENHO)
        self.assertEqual(codigos(est), ["step-without-design"])

    def test_step_without_design_isenta_rodada_revisao_fechamento_e_pedido(self):
        passos = passo("P1", titulo="A rodada de decisão", executa="Executa a rodada", est="1") + \
            passo("P2", titulo="O aceite", executa="Executa os `C`", est="1") + \
            passo("P3", titulo="Passo a pedido", executa="Executa a pedido de Anderson", est="1") + \
            passo("P4", titulo="O fechamento", executa="Executa o fechamento", est="1") + \
            passo("P5", titulo="A revisão da entrega", executa="Executa a revisão", est="1")
        est = self.estado(plano(passos, RODADA1, est="5", rest="5"), design=DESENHO)
        self.assertEqual(est["problemas"], [])

    def test_sem_desenho_nao_exige_executa_d(self):
        est = self.estado(plano(passo("P1", executa="Executor: a sessão"), RODADA1))
        self.assertEqual(est["problemas"], [])

    def test_step_cites_unknown_design(self):
        est = self.estado(plano(passo("P1", executa="Executa D1, D9"), RODADA1), design=DESENHO)
        self.assertEqual(codigos(est), ["step-cites-unknown-design"])

    def test_design_without_origin(self):
        d = DESENHO.replace("- **Origem:** R1.1\n", "")
        est = self.estado(plano(passo("P1"), RODADA1), design=d)
        self.assertEqual(codigos(est), ["design-without-origin"])
        self.assertEqual(est["problemas"][0]["onde"], "D2")

    def test_origin_unknown_round(self):
        d = DESENHO.replace("R1.1, R1.2", "R1.1, R7.3")
        est = self.estado(plano(passo("P1"), RODADA1), design=d)
        self.assertEqual(codigos(est), ["origin-unknown-round"])
        self.assertIn("R7.3", est["problemas"][0]["msg"])

    def test_origem_so_com_rodada_sem_pergunta(self):
        d = DESENHO.replace("R1.1, R1.2", "R1")
        self.assertEqual(self.estado(plano(passo("P1"), RODADA1), design=d)["problemas"], [])
        d = DESENHO.replace("R1.1, R1.2", "R5")
        self.assertEqual(codigos(self.estado(plano(passo("P1"), RODADA1), design=d)), ["origin-unknown-round"])

    def test_deviation_not_cited(self):
        desvios = "## Desvios\n\n- **X1 — O que mudou.** Por quê, e nada mais.\n"
        est = self.estado(plano(passo("P1"), RODADA1, desvios=desvios), design=DESENHO)
        self.assertEqual(codigos(est), ["deviation-not-cited"])
        self.assertEqual(est["problemas"][0]["nivel"], "aviso")

    def test_deviation_citado_pelo_passo_ou_nomeando_o_passo(self):
        desvios = "## Desvios\n\n- **X1 — O que mudou.** Afeta P1.\n- **X2 — Outro.** Sem passo.\n"
        extra = passo("P1") .replace("- [ ] **1. A**", "- [ ] **1. A** (o X2 entra aqui)")
        est = self.estado(plano(extra, RODADA1, desvios=desvios), design=DESENHO)
        self.assertEqual(est["problemas"], [])

    def test_duplicate_id(self):
        est = self.estado(plano(passo("P1") + passo("P1"), RODADA1, est="5", rest="5"), design=DESENHO)
        self.assertIn("duplicate-id", codigos(est))
        d = DESENHO + "\n### D1 — Repetido\n\n- **Origem:** R1.1\n"
        est = self.estado(plano(passo("P1"), RODADA1), design=d)
        self.assertEqual(codigos(est), ["duplicate-id"])
        est = self.estado(plano(passo("P1"), RODADA1 + "\n" + RODADA1), design=DESENHO)
        self.assertIn("duplicate-id", codigos(est))

    def test_alternativa_repetida_em_outro_d_nao_e_duplicada(self):
        d = DESENHO + "\n#### As alternativas\n\n##### A1 — Mais uma\n"
        est = self.estado(plano(passo("P1"), RODADA1), design=d)
        self.assertEqual(est["problemas"], [])
        self.assertIn("D2/A1", est["ids"]["A"])

    def test_proximo_respeita_depende_de(self):
        passos = passo("P1", est="1", executa="Executa D1") + \
            passo("P2", est="1", executa="Executa D1 · depende de P3") + passo("P3", est="1", executa="Executa D1")
        est = self.estado(plano(passos, RODADA1, est="3", rest="3"), design=DESENHO)
        self.assertEqual(est["proximo"], "P1")


class Fix(Base):
    def test_fix_reescreve_so_as_tres_horas(self):
        txt = plano(passo(est="2,5") + passo("P2", est="1,5"), RODADA1, est="9", exe="9", rest="9")
        raiz, path = self.monta(txt, design=DESENHO)
        rc, out, err = self.cli(path, "--fix")
        self.assertEqual(rc, 0, out)
        with open(path, encoding="utf-8") as f:
            novo = f.read()
        self.assertIn("estimate_h: 4\n", novo)
        self.assertIn("executed_h: 0\n", novo)
        self.assertIn("remaining_h: 4\n", novo)
        linhas_antes = [l for l in txt.split("\n") if not l.startswith(("estimate_h", "executed_h", "remaining_h"))]
        linhas_depois = [l for l in novo.split("\n") if not l.startswith(("estimate_h", "executed_h", "remaining_h"))]
        self.assertEqual(linhas_antes, linhas_depois)

    def test_fix_acrescenta_a_chave_ausente(self):
        fm = "---\nstatus: open\nphase: design\nready: sim\n---\n"
        raiz, path = self.monta(plano(passo(est="2"), RODADA1, fm=fm), design=DESENHO)
        self.cli(path, "--fix")
        fmt = plan_md.carrega(path).fm
        self.assertEqual((fmt["estimate_h"], fmt["executed_h"], fmt["remaining_h"]), ("2", "0", "2"))
        self.assertEqual(plan_state.estado(path)["problemas"], [])

    def test_strict_e_avisos(self):
        desvios = "## Desvios\n\n- **X1 — O que mudou.** Nada.\n"
        raiz, path = self.monta(plano(passo("P1"), RODADA1, desvios=desvios), design=DESENHO)
        self.assertEqual(self.cli(path)[0], 0)
        self.assertEqual(self.cli(path, "--strict")[0], 1)

    def test_next_sem_pendente(self):
        passos = passo("P1", exe="1 h", checks="- [x] **1. A**", evidencia=EV)
        raiz, path = self.monta(plano(passos, RODADA1, est="2.5", exe="1", rest="0"), design=DESENHO)
        rc, out, _ = self.cli(path, "--next")
        self.assertEqual((rc, out.strip()), (0, "nenhum"))


if __name__ == "__main__":
    unittest.main()
