import io
import json
import os
import shutil
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import close_check
from mini import DESENHO, RODADA1, passo, plano

EV = "`brza-workspace@a1b2c3d` · `python3 -m unittest` → 12 OK"
FEITO = passo("P1", est="5", exe="1 h", checks="- [x] **1. A**", evidencia=EV)
FM_FECHADO = "---\nstatus: done\nphase: closed\nready: sim\nestimate_h: 5\nexecuted_h: 1\nremaining_h: 0\n---\n"


def nota(status="done", h1="# Uma nota"):
    return "---\nstatus: %s\n---\n\n%s\n" % (status, h1)


def reviu(*achados, nome="REV-900"):
    t = "---\nstatus: done\n---\n\n# %s: o parecer\n\n" % nome
    for a in achados:
        t += a + "\n\n"
    return t


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def confere(self, texto, **k):
        raiz, path = _paths.plano_tmp(texto, **k)
        self.dirs.append(raiz)
        return close_check.confere(path), path

    def res(self, r):
        return {i["item"]: i["resultado"] for i in r["itens"]}

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = close_check.main(list(args))
        return rc, out.getvalue(), err.getvalue()


class Itens(Base):
    def test_plano_fechado_limpo(self):
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO), design=DESENHO)
        # R1.1 e R1.2 estão na Origem de algum D: nada a levar à casa dona
        self.assertEqual(self.res(r), {1: "ok", 2: "ok", 3: "ok", 4: "ok", 5: "n/a", 6: "n/a"})
        self.assertTrue(r["limpo"])

    def test_item1_passo_pendente_e_sem_evidencia(self):
        r, _ = self.confere(plano(passo("P1") + passo("P2", checks="- [x] **1. A**", exe="1 h", est="5"), RODADA1,
                                  est="10", exe="1", rest="5"), design=DESENHO)
        self.assertEqual(self.res(r)[1], "falta")
        det = " ".join(r["itens"][0]["detalhe"])
        self.assertIn("P1: pendente", det)
        self.assertIn("P2", det)
        self.assertFalse(r["limpo"])

    def test_item1_descartado_exige_motivo(self):
        sem = passo("P1", checks="- [-] **1. A**")
        com = passo("P1", checks="- [-] **1. A** — descartado porque o D1 mudou na R3")
        self.assertEqual(self.res(self.confere(plano(sem, RODADA1, est="5", rest="0"), design=DESENHO)[0])[1], "falta")
        self.assertEqual(self.res(self.confere(plano(com, RODADA1, est="5", rest="0"), design=DESENHO)[0])[1], "ok")

    def test_item1_sem_passos(self):
        r, _ = self.confere(plano("", RODADA1, fm=FM_FECHADO))
        self.assertEqual(self.res(r)[1], "falta")

    def test_item2_destinos(self):
        parecer = reviu(
            "### A1 — Corrige o que quebra\n\n> bug · importante · confiança 90 · → corrigido aqui\n\n**Evidência:** `a.py:1`",
            "### A2 — Vai a issue que existe\n\n> bug · sugestão · confiança 90 · → issue a-issue-boa\n\n**Evidência:** `a.py:2`",
            "### A3 — Falso\n\n> bug · importante · confiança 95 · → falso\n\n**Por que é falso:** x.",
            "### A4 — Título → descartado, por custo\n\n**Evidência:** `a.py:4`")
        rev = "\n## Revisões\n\n- [REV-900: o parecer](../../work/reviews/REV-900-p.md) — 2026-11-10, 4 achados.\n"
        extra = {"work/reviews/REV-900-p.md": parecer, "work/issues/a-issue-boa.md": nota("open")}
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=rev), design=DESENHO, extra=extra)
        self.assertEqual(self.res(r)[2], "ok", r["itens"][1])

    def test_item2_a_definir_e_destino_que_nao_existe(self):
        parecer = reviu(
            "### A1 — Sem destino\n\n> bug · importante · confiança 90 · → a definir\n\n**Evidência:** `a.py:1`",
            "### A2 — Issue fantasma\n\n> bug · sugestão · confiança 90 · → issue nao-existe\n\n**Evidência:** `a.py:2`",
            "### A3 — Sem a linha\n\n**Evidência:** `a.py:3`")
        rev = "\n## Revisões\n\n- [REV-900: o parecer](../../work/reviews/REV-900-p.md) — 2026-11-10.\n"
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=rev), design=DESENHO,
                            extra={"work/reviews/REV-900-p.md": parecer})
        self.assertEqual(self.res(r)[2], "falta")
        det = r["itens"][1]["detalhe"]
        self.assertEqual(len(det), 3)
        self.assertTrue(any("A1" in d and "a definir" in d for d in det))
        self.assertTrue(any("A2" in d and "nao-existe" in d for d in det))
        self.assertTrue(any("A3" in d for d in det))

    def test_item2_parecer_que_nao_existe(self):
        rev = "\n## Revisões\n\n- [REV-900: o parecer](../../work/reviews/REV-900-p.md) — 2026-11-10.\n"
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=rev), design=DESENHO)
        self.assertEqual(self.res(r)[2], "falta")

    def test_item3_decidida_sem_d_nem_link_e_manual(self):
        # a R1.1 foi decidida e nenhum D a cita; a R1.2 é resposta literal, e o D a cita
        d = DESENHO.replace("R1.1, R1.2", "R1.2").replace("- **Origem:** R1.1\n", "- **Origem:** R1.2\n")
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO), design=d)
        self.assertEqual(self.res(r)[3], "manual")
        self.assertEqual([c.split(" —")[0] for c in r["itens"][2]["detalhe"]], ["R1.1"])

    def test_item3_conta_a_resposta_em_texto_livre_lida_como_opcao(self):
        # A10: a R1.2 foi respondida por `Resposta:` com a leitura; sem D nem link, também vai ao Retomar
        d = DESENHO.replace("R1.1, R1.2", "R1.1")
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO), design=d)
        self.assertEqual([c.split(" —")[0] for c in r["itens"][2]["detalhe"]], ["R1.2"])

    def test_item3_contraproposta_nao_conta(self):
        rod = RODADA1.replace('lida como a primeira opção.', 'Lida como contraproposta: foi à rodada 2.')
        d = DESENHO.replace("R1.1, R1.2", "R1.1")
        r, _ = self.confere(plano(FEITO, rod, fm=FM_FECHADO), design=d)
        self.assertEqual(self.res(r)[3], "ok")

    def test_item3_link_em_decisoes_cobre(self):
        d = DESENHO.replace("R1.1, R1.2", "R1.2").replace("- **Origem:** R1.1\n", "- **Origem:** R1.2\n")
        dec = "\n## Decisões\n\n- [Uma nota](../../work/decisions/uma.md) — R1.1, `done`.\n"
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=dec), design=d,
                            extra={"work/decisions/uma.md": nota("done")})
        self.assertEqual(self.res(r)[3], "ok")

    def test_item4_decisoes_done(self):
        dec = "\n## Decisões\n\n- [A boa](../../work/decisions/a.md) — R1.1, `done`.\n- [A aberta](../../work/decisions/b.md) — R1.2.\n"
        extra = {"work/decisions/a.md": nota("done"), "work/decisions/b.md": nota("proposed")}
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=dec), design=DESENHO, extra=extra)
        self.assertEqual(self.res(r)[4], "falta")
        self.assertEqual(len(r["itens"][3]["detalhe"]), 1)
        self.assertIn("b.md", r["itens"][3]["detalhe"][0])
        dec2 = "\n## Decisões\n\n- [A boa](../../work/decisions/a.md) — R1.1, `done`.\n- [Fantasma](../../work/decisions/z.md).\n"
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=dec2), design=DESENHO, extra=extra)
        self.assertEqual(self.res(r)[4], "falta")

    def test_item5_commit_do_studio_e_manual(self):
        ev = "`brza-studio@a1b2c3d` · `pnpm test` → 12 OK"
        p = passo("P1", est="5", exe="1 h", checks="- [x] **1. A**", evidencia=ev)
        r, _ = self.confere(plano(p, RODADA1, fm=FM_FECHADO), design=DESENHO)
        self.assertEqual(self.res(r)[5], "manual")
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO), design=DESENHO)
        self.assertEqual(self.res(r)[5], "n/a")

    def test_item6_janela(self):
        sem = "\n## Janela\n\n- **Janela e meta:** de 2026-11-09 a 2026-11-12; o painel publica sozinho.\n- **Cortes previstos:** o P9.\n"
        com = sem + "- **Fecho:** a meta foi cumprida em 2026-11-11; `executed_h` 1 contra `estimate_h` 5.\n"
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=sem), design=DESENHO)
        self.assertEqual(self.res(r)[6], "falta")
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=com), design=DESENHO)
        self.assertEqual(self.res(r)[6], "ok")
        nao = sem + "A meta não foi cumprida: o P9 ficou de fora.\n"
        r, _ = self.confere(plano(FEITO, RODADA1, fm=FM_FECHADO, extra=nao), design=DESENHO)
        self.assertEqual(self.res(r)[6], "ok")


class Cli(Base):
    def test_exit_0_com_manual_e_1_com_falta(self):
        raiz, path = _paths.plano_tmp(plano(FEITO, RODADA1, fm=FM_FECHADO), design=DESENHO)
        self.dirs.append(raiz)
        rc, out, _ = self.cli(path)
        self.assertEqual(rc, 0)
        self.assertIn("fechamento: pode seguir", out)
        raiz, path = _paths.plano_tmp(plano(passo("P1"), RODADA1), design=DESENHO)
        self.dirs.append(raiz)
        rc, out, _ = self.cli(path, "--json")
        self.assertEqual(rc, 1)
        self.assertFalse(json.loads(out)["limpo"])

    def test_pln021_real_aberto_trava(self):
        rc, out, _ = self.cli(os.path.join(_paths.RAIZ, "plans", "PLN-021-o-plano-coordenado-e-os-artboards", "PLN-021-plan.md"))
        self.assertEqual(rc, 1)
        self.assertIn("P1: pendente", out)

    def test_pln017_real(self):
        rc, out, _ = self.cli(os.path.join(_paths.RAIZ, "plans", "PLN-017-a-reuniao-multiagente-como-fluxo-replicavel", "PLN-017-plan.md"), "--json")
        r = json.loads(out)
        self.assertEqual(rc, 1)
        res = {i["item"]: i["resultado"] for i in r["itens"]}
        self.assertEqual(res[1], "falta")  # a evidência da P7 não traz commit, `→` nem arquivo:linha
        self.assertEqual(res[4], "ok")
        self.assertEqual(res[5], "n/a")
        self.assertEqual(res[6], "n/a")

    def test_uso(self):
        self.assertEqual(self.cli()[0], 2)
        self.assertEqual(self.cli("PLN-999-nao-existe")[0], 2)


if __name__ == "__main__":
    unittest.main()
