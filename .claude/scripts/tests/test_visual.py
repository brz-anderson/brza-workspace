"""Testes do skillkit.visual: o `.html` do `::orca-visual` e o PNG (`brza shot` primeiro, Chrome de reserva)."""
import os
import tempfile
import unittest

import _paths  # noqa: F401
from skillkit import visual


class Salva(unittest.TestCase):
    def test_com_publish_dir_o_nome_e_fixo_para_a_mesma_chave(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, linha = visual.salva_visual("<p>1</p>", "mcp", "r3", "3", 'Rodada "3" {x}', publish_dir=tmp)
            b, _ = visual.salva_visual("<p>2</p>", "mcp", "r3", "3", "outro", publish_dir=tmp)
            c, _ = visual.salva_visual("<p>2</p>", "mcp", "r3", "4", "outro", publish_dir=tmp)
            self.assertEqual(a, b)
            self.assertNotEqual(a, c)
            self.assertRegex(os.path.basename(a), r"^mcp-r3-[0-9a-f]{4}\.html$")
            self.assertEqual(linha, f'::orca-visual{{file="{os.path.basename(a)}" title="Rodada 3 x"}}')
            with open(b, encoding="utf-8") as f:
                self.assertEqual(f.read(), "<p>2</p>")

    def test_sem_publish_dir_grava_no_alvo_padrao(self):
        with tempfile.TemporaryDirectory() as tmp:
            alvo = os.path.join(tmp, "x.html")
            self.assertEqual(visual.salva_visual("<i/>", "id", "r1", "1", "t", alvo_padrao=alvo), (alvo, None))
            self.assertTrue(os.path.isfile(alvo))

    def test_recusa_o_grande_e_o_prefixo_com_caminho(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(visual.ErroPublicacao) as c:
                visual.salva_visual("x" * visual.LIMITE_HTML, "id", "r", "1", "t", publish_dir=tmp)
            self.assertIn("512 KB", str(c.exception))
            for ruim in ("../x", "a/b", "a\\b"):
                with self.assertRaises(visual.ErroPublicacao):
                    visual.salva_visual("x", ruim, "r", "1", "t", publish_dir=tmp)
            self.assertEqual(os.listdir(tmp), [])

    def test_titulo_seguro(self):
        self.assertEqual(visual.titulo_seguro('a\n"b"  {c}\\d'), "a b c d")
        self.assertEqual(visual.titulo_seguro(None), "")


class Png(unittest.TestCase):
    def setUp(self):
        self.run, self.chrome, self.CHROME = visual._run, visual._chrome, visual.CHROME
        self.chamadas = []
        self.tmp = tempfile.TemporaryDirectory()
        self.html = os.path.join(self.tmp.name, "a.html")
        self.png = os.path.join(self.tmp.name, "a.png")
        with open(self.html, "w", encoding="utf-8") as f:
            f.write("<p>oi</p>")

    def tearDown(self):
        visual._run, visual._chrome, visual.CHROME = self.run, self.chrome, self.CHROME
        self.tmp.cleanup()

    def runner(self, rc, grava=True, err=""):
        def fake(argv, timeout=60):
            self.chamadas.append(argv)
            if rc == 0 and grava:
                open(self.png, "wb").close()
            return rc, "", err
        visual._run = fake

    def test_usa_o_brza_shot_com_largura_tema_escala_e_force(self):
        self.runner(0)
        self.assertIsNone(visual.gera_png(self.html, self.png, 736))
        self.assertEqual(self.chamadas, [[visual.BRZA, "shot", os.path.abspath(self.html), self.png, "--width", "736",
                                          "--theme", "light", "--scale", "1", "--force"]])

    def test_tema_e_escala_passam(self):
        self.runner(0)
        visual.gera_png(self.html, self.png, 600, 4200, theme="dark", scale=2)
        self.assertEqual(self.chamadas[0][-5:], ["--theme", "dark", "--scale", "2", "--force"])

    def test_a_altura_nao_vai_ao_brza_shot(self):
        self.runner(0)
        visual.gera_png(self.html, self.png, 736, 4200)
        self.assertNotIn("4200", self.chamadas[0])

    def test_brza_que_falha_cai_no_chrome(self):
        self.runner(2, err="boom")
        visto = {}

        def chrome(html, png, width, altura, scale):
            visto["args"] = (html, png, width, altura, scale)
            open(png, "wb").close()
            return None
        visual._chrome = chrome
        self.assertIsNone(visual.gera_png(self.html, self.png, 736, 4200))
        self.assertEqual(visto["args"], (self.html, self.png, 736, 4200, 1))

    def test_css_de_reserva_so_vai_ao_chrome_e_o_brza_recebe_o_html_intacto(self):
        # A14: o `brza shot` injeta os tokens do chat; um `:root` no HTML venceria o tema dele
        self.runner(0)
        self.assertIsNone(visual.gera_png(self.html, self.png, 736, chrome_css=":root{--x:1}"))
        self.assertEqual(self.chamadas[0][2], os.path.abspath(self.html))
        with open(self.html, encoding="utf-8") as f:
            self.assertEqual(f.read(), "<p>oi</p>")
        os.remove(self.png)
        self.runner(2, err="boom")
        visto = {}

        def chrome(html, png, width, altura, scale):
            with open(html, encoding="utf-8") as f:
                visto["texto"], visto["html"] = f.read(), html
            open(png, "wb").close()
            return None
        visual._chrome = chrome
        self.assertIsNone(visual.gera_png(self.html, self.png, 736, chrome_css=":root{--x:1}"))
        self.assertIn("<style>:root{--x:1}</style>", visto["texto"])
        self.assertNotEqual(visto["html"], self.html)
        self.assertFalse(os.path.exists(visto["html"]))      # o temporário não fica

    def test_brza_ausente_cai_no_chrome_com_a_altura_padrao(self):
        self.runner(127, err="No such file")
        visto = {}
        visual._chrome = lambda h, p, w, a, s: visto.update(altura=a) or None
        self.assertIsNone(visual.gera_png(self.html, self.png, 736))
        self.assertEqual(visto["altura"], visual.ALTURA_CHROME)

    def test_as_duas_falhas_aparecem_no_erro(self):
        self.runner(2, err="boom")
        visual._chrome = lambda *a: "Chrome não encontrado; sem PNG"
        erro = visual.gera_png(self.html, self.png, 736)
        self.assertIn("brza shot falhou (rc 2): boom", erro)
        self.assertIn("Chrome não encontrado", erro)

    def test_brza_rc0_sem_arquivo_tambem_cai(self):
        self.runner(0, grava=False)
        visual._chrome = lambda *a: "o Chrome não gerou o PNG"
        erro = visual.gera_png(self.html, self.png, 736)
        self.assertIn("o brza não gerou o PNG", erro)

    def test_chrome_real_de_reserva_monta_o_comando(self):
        visual.CHROME = __file__  # existe, mas não é o Chrome: o runner trocado vê o comando
        self.runner(0, grava=False)
        visual._run = lambda argv, timeout=60: (self.chamadas.append(argv), (0, "", ""))[1]
        erro = visual._chrome(self.html, self.png, 700, 1500, 1)
        self.assertEqual(erro, "o Chrome não gerou o PNG")
        self.assertIn("--window-size=700,1500", self.chamadas[0])
        self.assertIn("--force-device-scale-factor=1", self.chamadas[0])
        visual.CHROME = "/nao/existe"
        self.assertIn("não encontrado", visual._chrome(self.html, self.png, 700, 1500, 1))


if __name__ == "__main__":
    unittest.main()
