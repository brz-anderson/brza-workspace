import json
import os

import _exec
import _paths  # noqa: F401
import consult
from mini import DESENHO, RODADA1, passo, plano

FIM = "<!-- fim-D1: %s -->"


class Consultores(_exec.Base):
    def setUp(self):
        super().setUp()
        self.raiz, self.path = self.monta()
        self.brief = os.path.join(self.raiz, "brief.md")
        with open(self.brief, "w", encoding="utf-8") as f:
            f.write("# Brief\n\nTerreno: x.\nCasos: um, dois.\n")
        self.cota = {"claude": 20, "codex": 30, "grok": 10}
        self.brza = lambda argv: (0, json.dumps({k: {"session_pct": v} for k, v in self.cota.items()}), "")

    def abre(self, *extra):
        return self.roda(consult, "open", self.path, "D1", "--brief", self.brief, "--no-panel", *extra)

    def man(self):
        with open(os.path.join(self.raiz, ".sessions", "pln-900", "D1", "consultores.json"), encoding="utf-8") as f:
            return json.load(f)

    def grava(self, foco, corpo, marcador=True):
        p = os.path.join(self.raiz, ".sessions", "pln-900", "D1", foco + ".md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(corpo + ("\n" + FIM % foco + "\n" if marcador else ""))

    def test_roster_padrao_abre_tres_em_runtimes_diferentes(self):
        self.assertEqual(self.abre(), 0, self.err)
        abertas = [a for k, a in self.chamadas if k == "sessions"]
        self.assertEqual([a[a.index("--agent") + 1] for a in abertas], ["claude", "codex", "grok"])
        self.assertEqual(abertas[0][abertas[0].index("--model") + 1], "claude-opus-5-5")
        self.assertEqual(abertas[0][abertas[0].index("--effort") + 1], "high")
        self.assertEqual(abertas[0][0], "pln900-d1-arquitetura-limpa")
        self.assertNotIn("--model", abertas[1])
        self.assertEqual(abertas[0][abertas[0].index("--checkout") + 1], self.raiz)
        self.assertIn("| arquitetura-limpa | pln900-d1-arquitetura-limpa | Claude |", self.out)
        self.assertEqual(sorted(self.man()["focos"]), ["arquitetura-limpa", "equilibrio", "mudanca-minima"])

    def test_prompt_comeca_pelo_consultor_e_manda_gravar_so_o_arquivo(self):
        self.abre()
        with open(os.path.join(self.raiz, ".sessions", "pln-900", "D1", "prompt-mudanca-minima.md"), encoding="utf-8") as f:
            t = f.read()
        self.assertTrue(t.startswith("Você é consultor do Desenho de D1 do PLN-900"))
        self.assertIn("Terreno: x.", t)
        self.assertIn("Grave SÓ o arquivo", t)
        self.assertIn("<!-- fim-D1: mudanca-minima -->", t)
        self.assertIn("Não envie `worker_done`", t)

    def test_cota_acima_de_55_troca_pelo_fallback(self):
        self.cota["codex"] = 56
        self.abre()
        abertas = [a for k, a in self.chamadas if k == "sessions"]
        self.assertEqual(abertas[1][abertas[1].index("--agent") + 1], "claude")
        self.assertEqual(abertas[1][abertas[1].index("--model") + 1], "claude-sonnet-5-5")
        self.assertIn("cota: codex cortado: codex a 56%", self.out)
        self.assertEqual(self.man()["focos"]["mudanca-minima"]["agent"], "claude")

    def test_cota_igual_a_55_entra(self):
        self.cota["claude"] = 55
        self.abre()
        self.assertEqual([a[a.index("--agent") + 1] for k, a in self.chamadas if k == "sessions"][0], "claude")

    def test_sem_quota_avisa_e_nao_corta(self):
        self.brza = lambda argv: (1, "", "falhou")
        self.assertEqual(self.abre(), 0)
        self.assertIn("não li o `brza quota --json`", self.err)

    def test_roster_proprio(self):
        r = os.path.join(self.raiz, "r.json")
        with open(r, "w") as f:
            json.dump({"consultores": [{"foco": "a", "agent": "grok"}, {"foco": "b", "agent": "grok"}]}, f)
        self.abre("--roster", r)
        self.assertEqual(sorted(self.man()["focos"]), ["a", "b"])
        with open(r, "w") as f:
            f.write("[]")
        self.assertEqual(self.abre("--roster", r), 2)

    def test_dry_run_nao_abre(self):
        self.assertEqual(self.abre("--dry-run"), 0)
        self.assertEqual([k for k, _ in self.chamadas if k == "sessions"], [])
        self.assertIn("[dry-run] brza sessions pln900-d1-arquitetura-limpa", self.out)
        self.assertFalse(os.path.exists(os.path.join(self.raiz, ".sessions")))

    def test_nao_abriu_para_o_lote(self):
        self.sessions = lambda argv: (1, "", "CHECK: x não abriu: pending-1.json")
        self.assertEqual(self.abre(), 1)
        self.assertEqual(len([1 for k, _ in self.chamadas if k == "sessions"]), 1)

    def test_decisao_inexistente_e_brief_ausente(self):
        self.assertEqual(self.roda(consult, "open", self.path, "D9", "--brief", self.brief), 2)
        self.assertEqual(self.roda(consult, "open", self.path, "D1", "--brief", "/nao/existe.md"), 2)

    def test_wait_narra_cada_chegada_e_chega_a_zero(self):
        self.abre()
        self.grava("arquitetura-limpa", "Tese: a.")
        self.grava("mudanca-minima", "Tese: b.")
        self.grava("equilibrio", "Tese: c.")
        self.assertEqual(self.roda(consult, "wait", self.path, "D1"), 0)
        self.assertEqual(self.out.count("entregou"), 3)
        self.assertIn("D1 · 3/3 — entregaram", self.out)

    def test_wait_prazo_75_lista_quem_falta(self):
        self.abre()
        self.grava("equilibrio", "Tese: c.")
        self.assertEqual(self.roda(consult, "wait", self.path, "D1", "--timeout", "20"), 75)
        self.assertIn("prazo: faltam arquitetura-limpa, mudanca-minima", self.out)

    def test_wait_arquivo_sem_marcador_nao_vale_e_falha_da_sessao(self):
        self.abre()
        self.grava("equilibrio", "Tese: c.", marcador=False)
        self.wait = lambda nomes, t, markers=(), any_=True: (0, {"done": [{"name": "pln900-d1-equilibrio", "outcome": "done"}], "timed_out": False, "events": []})
        self.assertEqual(self.roda(consult, "wait", self.path, "D1", "--timeout", "30"), 75)
        self.assertIn("o turno acabou sem o marcador", self.out)
        self.wait = lambda nomes, t, markers=(), any_=True: (1, {"done": [{"name": "pln900-d1-equilibrio", "outcome": "failed"}], "timed_out": False, "events": []})
        self.assertEqual(self.roda(consult, "wait", self.path, "D1", "--timeout", "30"), 1)

    def test_tabela_lado_a_lado_com_os_tres_arquivos(self):
        self.abre()
        self.grava("arquitetura-limpa", "Tese: JSON.\n\n- **Caso 1:** Custo: 3 h · Se paga: já · Reabre: o schema\n- **Caso 2:** Custo: 1 h · Se paga: com anexo · Reabre: nada\n\nRisco: ninguém abre JSON.")
        self.grava("mudanca-minima", "Tese: Markdown.\n\n**Custo:** 1 h\n**Se paga:** agora\n**Reabre:** o importador\nRisco: sem metadado\n  que continua aqui.")
        self.grava("equilibrio", "Tese: YAML.\nCusto: 2 h · Se paga: já · Reabre: pouco\nRisco: formato novo")
        pub = os.path.join(self.raiz, "pub")
        self.assertEqual(self.roda(consult, "table", self.path, "D1", "--publish-dir", pub), 0, self.err)
        linhas = self.saidas[0].split("\n")
        self.assertEqual(linhas[0], "| | arquitetura-limpa (Claude) | mudanca-minima (Codex) | equilibrio (Grok) |")
        self.assertIn("| **Custo** | 3 h / 1 h | 1 h | 2 h |", linhas)
        self.assertIn("| **Se paga** | já / com anexo | agora | já |", linhas)
        self.assertIn("| **Reabre** | o schema / nada | o importador | pouco |", linhas)
        self.assertIn("| **Risco** | ninguém abre JSON. | sem metadado que continua aqui. | formato novo |", linhas)
        self.assertRegex(self.saidas[-1], r'^::orca-visual\{file="pln-900-d1-[0-9a-f]{4}\.html" title="PLN-900 D1')
        nome = self.saidas[-1].split('"')[1]
        with open(os.path.join(pub, nome), encoding="utf-8") as f:
            self.assertIn("arquitetura-limpa", f.read())

    def test_tabela_com_foco_que_nao_entregou(self):
        self.abre()
        self.grava("equilibrio", "Tese: YAML.\nCusto: 2 h")
        self.roda(consult, "table", self.path, "D1", "--publish-dir", os.path.join(self.raiz, "pub"))
        self.assertIn("(não entregou)", self.out)
        self.assertIn("sem arquivo com o marcador", self.err)
        self.assertIn("o arquivo não traz `Se paga:`", self.err)

    def test_close_um_por_um(self):
        self.abre()
        self.sessions = lambda argv: (0, json.dumps({"status": "released"}), "")
        self.assertEqual(self.roda(consult, "close", self.path, "D1"), 0)
        self.assertEqual({v["estado"] for v in self.man()["focos"].values()}, {"fechado"})
        fechos = [a for k, a in self.chamadas if k == "sessions" and a[0] == "close"]
        self.assertEqual(len(fechos), 3)
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.assertIn("NÃO está fechada", (self.roda(consult, "close", self.path, "D1"), self.out)[1])

    def test_pipe_na_celula_nao_quebra_a_tabela(self):
        self.assertEqual(consult.cel("a | b\nc"), "a \\| b c")


if __name__ == "__main__":
    import unittest
    unittest.main()
