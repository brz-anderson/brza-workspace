import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import plan_md
import plan_state
import round_log
from mini import DESENHO, RODADA1, passo, plano

PLN21 = os.path.join("plans", "PLN-021-o-plano-coordenado-e-os-artboards", "PLN-021-plan.md")


def rodada(**k):
    d = {
        "titulo": "o P2 volta com desvios", "enviada": "2026-11-10",
        "apresentado_antes": "O implementer devolveu o P2.\nTrês desvios.",
        "respondida": {"data": "2026-11-10", "sessao": "a sessão do workstream playground"},
        "perguntas": [{
            "tema": "O commit do executor", "multipla": False,
            "opcoes": [
                {"rotulo": "o pedido autoriza o commit na branch do passo", "recomendada": True,
                 "custo": "muda a regra de hoje", "se_paga": "em todo passo"},
                {"rotulo": "o executor para antes do commit", "custo": "uma rodada por passo", "se_paga": "agora"},
            ],
            "resposta": {"escolhidas": [0], "literal": None}, "reabre": None,
        }],
    }
    d.update(k)
    return d


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def copia(self):
        r = _paths.copia_raiz()
        self.dirs.append(os.path.dirname(r))
        return r, os.path.join(r, PLN21)

    def monta(self, *a, **k):
        raiz, path = _paths.plano_tmp(*a, **k)
        self.dirs.append(raiz)
        return raiz, path

    def json(self, dados):
        d = tempfile.mkdtemp(prefix="rl-")
        self.dirs.append(d)
        p = os.path.join(d, "rodada.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        return p

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = round_log.main(list(args) + ["--no-panel"])
        return rc, out.getvalue(), err.getvalue()

    def le(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()


class Proxima(Base):
    def test_next(self):
        raiz, path = self.copia()
        rc, out, _ = self.cli(path, "--next")
        self.assertEqual((rc, out.strip()), (0, "5"))

    def test_next_sem_rodada(self):
        raiz, path = self.monta(plano(passo(), ""))
        self.assertEqual(self.cli(path, "--next")[1].strip(), "1")


class Grava(Base):
    def test_decidida_acrescenta_no_fim_da_entrevista(self):
        raiz, path = self.copia()
        antes = self.le(path)
        rc, out, err = self.cli(path, "--from", self.json(rodada()))
        self.assertEqual(rc, 0, err)
        self.assertEqual(os.path.realpath(out.strip()), os.path.realpath(path))
        novo = self.le(path)
        self.assertIn("### Rodada 5 — o P2 volta com desvios (enviada 2026-11-10)", novo)
        self.assertIn("> **Apresentado antes:** O implementer devolveu o P2.\n> Três desvios.", novo)
        self.assertIn("Respondida em 2026-11-10, na sessão do workstream playground.", novo)
        self.assertIn("1. **O commit do executor.** Opções:", novo)
        self.assertIn("   - o pedido autoriza o commit na branch do passo (recomendada) — custo: muda a regra de hoje; "
                      "se paga: em todo passo;", novo)
        self.assertIn("   - o executor para antes do commit — custo: uma rodada por passo; se paga: agora.", novo)
        self.assertIn("   **Decidido — o pedido autoriza o commit na branch do passo.**", novo)
        # a rodada entra antes de `## Passos`, e o resto do arquivo não muda
        self.assertLess(novo.index("### Rodada 5"), novo.index("\n## Passos\n"))
        self.assertGreater(novo.index("### Rodada 5"), novo.index("### Rodada 4"))
        removido = [l for l in novo.split("\n") if l not in antes.split("\n")]
        self.assertTrue(all(l.strip() == "" or "Rodada 5" in l or l.startswith(("> ", "Respondida", "1. ", "   ")) for l in removido))
        # relê como rodada decidida
        pl = plan_md.carrega(path)
        q = pl.pergunta("R5.1")
        self.assertTrue(q.decidida)
        self.assertEqual(q.tema, "O commit do executor")
        self.assertEqual([o["recomendada"] for o in q.opcoes()], [True, False])
        self.assertEqual(plan_state.estado(path)["problemas"], [])

    def test_literal_vai_como_resposta_com_a_leitura(self):
        raiz, path = self.copia()
        d = rodada()
        d["perguntas"][0]["resposta"] = {"escolhidas": None, "literal": "para antes do commit, sempre"}
        self.cli(path, "--from", self.json(d))
        q = plan_md.carrega(path).pergunta("R5.1")
        self.assertFalse(q.decidida)
        self.assertIn('**Resposta:** "para antes do commit, sempre"', q.resposta)

    def test_literal_com_escolhida_lida_como(self):
        raiz, path = self.copia()
        d = rodada()
        d["perguntas"][0]["resposta"] = {"escolhidas": [1], "literal": "a segunda"}
        self.cli(path, "--from", self.json(d))
        q = plan_md.carrega(path).pergunta("R5.1")
        self.assertIn('"a segunda" Lida como: o executor para antes do commit.', q.resposta)
        self.assertIsNone(q.decidido)

    def test_sem_resposta(self):
        raiz, path = self.copia()
        d = rodada(respondida=None)
        d["perguntas"][0]["resposta"] = None
        self.cli(path, "--from", self.json(d))
        pl = plan_md.carrega(path)
        self.assertTrue(pl.rodada(5).sem_resposta)
        self.assertFalse(pl.pergunta("R5.1").decidida)

    def test_multipla(self):
        raiz, path = self.copia()
        d = rodada()
        d["perguntas"][0]["multipla"] = True
        d["perguntas"][0]["resposta"] = {"escolhidas": [0, 1], "literal": None}
        self.cli(path, "--from", self.json(d))
        novo = self.le(path)
        self.assertIn("1. **O commit do executor** (seleção múltipla). Opções:", novo)
        self.assertIn("**Decidido — o pedido autoriza o commit na branch do passo; o executor para antes do commit.**", novo)

    def test_reabre_marca_a_linha_antiga(self):
        raiz, path = self.copia()
        d = rodada()
        d["perguntas"][0]["reabre"] = "R1.2"
        rc, out, err = self.cli(path, "--from", self.json(d))
        self.assertEqual(rc, 0, err)
        pl = plan_md.carrega(path)
        self.assertEqual(pl.pergunta("R1.2").reaberta, "R3.1")  # a R1.2 já estava reaberta em R3.1: a marca nova vai junto
        self.assertIn("**→ reaberta em R5.1**", pl.pergunta("R1.2").bloco)
        linhas = [l for l in self.le(path).split("\n") if "reaberta em R5.1" in l]
        self.assertEqual(len(linhas), 1)
        self.assertTrue(linhas[0].lstrip().startswith("**Decidido — protótipo no playground.**"))

    def test_reabre_sem_linha_decidido_vai_na_ultima_linha(self):
        raiz, path = self.copia()
        d = rodada()
        d["perguntas"][0]["reabre"] = "R4.1"  # a R4.1 não tem Decidido
        self.cli(path, "--from", self.json(d))
        q = plan_md.carrega(path).pergunta("R4.1")
        self.assertIn("reaberta em R5.1", q.bloco)
        self.assertEqual(q.reaberta, "R5.1")
        self.assertEqual(plan_md.carrega(path).pergunta("R4.2").reaberta, None)

    def test_dry_run_nao_grava(self):
        raiz, path = self.copia()
        antes = self.le(path)
        d = rodada()
        d["perguntas"][0]["reabre"] = "R1.2"
        rc, out, err = self.cli(path, "--from", self.json(d), "--dry-run")
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.le(path), antes)
        self.assertIn("# dry-run: Rodada 5", out)
        self.assertIn("### Rodada 5 — o P2 volta com desvios", out)
        self.assertIn("# marcaria R1.2 com `→ reaberta em R5.1`", out)

    def test_dois_registros_seguidos_numeram_6(self):
        raiz, path = self.copia()
        self.cli(path, "--from", self.json(rodada()))
        self.cli(path, "--from", self.json(rodada(titulo="a segunda")))
        pl = plan_md.carrega(path)
        self.assertEqual([r.n for r in pl.rodadas()], [1, 2, 3, 4, 5, 6])
        self.assertEqual(plan_state.estado(path)["problemas"], [])

    def test_plano_dividido_grava_no_interview(self):
        inter = "# PLN-900 — Entrevista\n\n" + RODADA1.replace("###", "##") + "\n"
        raiz, path = self.monta(plano(passo()).replace("## Entrevista\n", ""), interview=inter)
        pasta = os.path.dirname(path)
        antes_plan = self.le(path)
        d = rodada(titulo="a nova")
        d["perguntas"][0]["reabre"] = "R1.1"
        rc, out, err = self.cli(path, "--from", self.json(d))
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.le(path), antes_plan)
        arq = os.path.join(pasta, "PLN-900-interview.md")
        self.assertEqual(os.path.realpath(out.strip()), os.path.realpath(arq))
        novo = self.le(arq)
        self.assertIn("## Rodada 2 — a nova (enviada 2026-11-10)", novo)
        self.assertTrue(novo.endswith("\n"))
        pl = plan_md.carrega(path)
        self.assertEqual(pl.pergunta("R1.1").reaberta, "R2.1")

    def test_enviada_ausente_vira_hoje(self):
        raiz, path = self.copia()
        d = rodada()
        d.pop("enviada")
        self.cli(path, "--from", self.json(d))
        import datetime
        self.assertIn("(enviada %s)" % datetime.date.today().isoformat(), self.le(path))


class Forma(Base):
    def casos(self):
        base = rodada()
        sem_titulo = dict(base, titulo="")
        sem_perguntas = dict(base, perguntas=[])
        so = json.loads(json.dumps(base))
        so["perguntas"][0]["opcoes"] = []
        idx = json.loads(json.dumps(base))
        idx["perguntas"][0]["resposta"] = {"escolhidas": [5], "literal": None}
        multi = json.loads(json.dumps(base))
        multi["perguntas"][0]["resposta"] = {"escolhidas": [0, 1], "literal": None}
        reabre = json.loads(json.dumps(base))
        reabre["perguntas"][0]["reabre"] = "R9.9"
        reabre_mal = json.loads(json.dumps(base))
        reabre_mal["perguntas"][0]["reabre"] = "a R1"
        data = dict(base, enviada="ontem")
        resp = dict(base, respondida={"data": "x"})
        return {"titulo": sem_titulo, "perguntas": sem_perguntas, "opcoes": so, "índice": idx, "multipla": multi,
                "reabre inexistente": reabre, "reabre fora da forma": reabre_mal, "data": data, "respondida": resp,
                "não é objeto": ["x"]}

    def test_json_fora_da_forma_sai_1_e_nao_grava(self):
        raiz, path = self.copia()
        antes = self.le(path)
        for nome, dados in self.casos().items():
            rc, out, err = self.cli(path, "--from", self.json(dados))
            self.assertEqual(rc, 1, nome)
            self.assertTrue(err.strip(), nome)
            self.assertEqual(self.le(path), antes, nome)

    def test_json_ilegivel_e_arquivo_ausente(self):
        raiz, path = self.copia()
        d = tempfile.mkdtemp(prefix="rl-")
        self.dirs.append(d)
        ruim = os.path.join(d, "ruim.json")
        with open(ruim, "w") as f:
            f.write("{nao e json")
        self.assertEqual(self.cli(path, "--from", ruim)[0], 1)
        self.assertEqual(self.cli(path, "--from", os.path.join(d, "nao-existe.json"))[0], 1)

    def test_uso(self):
        self.assertEqual(self.cli()[0], 2)
        self.assertEqual(self.cli("PLN-999-que-nao-existe", "--next")[0], 2)

    def test_plano_sem_entrevista_recusa(self):
        raiz, path = self.monta(plano(passo()).replace("## Entrevista\n", ""))
        rc, out, err = self.cli(path, "--from", self.json(rodada()))
        self.assertEqual(rc, 1)
        self.assertIn("Entrevista", err)


if __name__ == "__main__":
    unittest.main()
