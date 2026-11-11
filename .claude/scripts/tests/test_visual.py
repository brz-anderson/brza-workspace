"""Testes do skillkit.visual: o `.html` do `::orca-visual` e o PNG (`brza shot` primeiro, Chrome de reserva)."""
import os
import tempfile
import unittest

import _paths  # noqa: F401
from skillkit import visual


class SavesVisual(unittest.TestCase):
    def test_with_publish_dir_the_name_is_fixed_for_the_same_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, line = visual.save_visual("<p>1</p>", "mcp", "r3", "3", 'Rodada "3" {x}', publish_dir=tmp)
            b, _ = visual.save_visual("<p>2</p>", "mcp", "r3", "3", "outro", publish_dir=tmp)
            c, _ = visual.save_visual("<p>2</p>", "mcp", "r3", "4", "outro", publish_dir=tmp)
            self.assertEqual(a, b)
            self.assertNotEqual(a, c)
            self.assertRegex(os.path.basename(a), r"^mcp-r3-[0-9a-f]{4}\.html$")
            self.assertEqual(line, f'::orca-visual{{file="{os.path.basename(a)}" title="Rodada 3 x"}}')
            with open(b, encoding="utf-8") as f:
                self.assertEqual(f.read(), "<p>2</p>")

    def test_without_publish_dir_writes_to_the_default_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            saved_path = os.path.join(tmp, "x.html")
            self.assertEqual(visual.save_visual("<i/>", "id", "r1", "1", "t", default_path=saved_path), (saved_path, None))
            self.assertTrue(os.path.isfile(saved_path))

    def test_refuses_the_large_and_the_prefix_with_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(visual.PublishError) as c:
                visual.save_visual("x" * visual.LIMIT_HTML, "id", "r", "1", "t", publish_dir=tmp)
            self.assertIn("512 KB", str(c.exception))
            for bad in ("../x", "a/b", "a\\b"):
                with self.assertRaises(visual.PublishError):
                    visual.save_visual("x", bad, "r", "1", "t", publish_dir=tmp)
            self.assertEqual(os.listdir(tmp), [])

    def test_title_safe(self):
        self.assertEqual(visual.safe_title('a\n"b"  {c}\\d'), "a b c d")
        self.assertEqual(visual.safe_title(None), "")


class Png(unittest.TestCase):
    def setUp(self):
        self.run, self.chrome, self.CHROME = visual._run, visual._chrome, visual.CHROME
        self.calls = []
        self.tmp = tempfile.TemporaryDirectory()
        self.html = os.path.join(self.tmp.name, "a.html")
        self.png = os.path.join(self.tmp.name, "a.png")
        with open(self.html, "w", encoding="utf-8") as f:
            f.write("<p>oi</p>")

    def tearDown(self):
        visual._run, visual._chrome, visual.CHROME = self.run, self.chrome, self.CHROME
        self.tmp.cleanup()

    def runner(self, rc, writes=True, err=""):
        def fake(argv, timeout=60):
            self.calls.append(argv)
            if rc == 0 and writes:
                open(self.png, "wb").close()
            return rc, "", err
        visual._run = fake

    def test_uses_the_brza_shot_with_width_theme_scale_and_force(self):
        self.runner(0)
        self.assertIsNone(visual.render_png(self.html, self.png, 736))
        self.assertEqual(self.calls, [[visual.BRZA, "shot", os.path.abspath(self.html), self.png, "--width", "736",
                                          "--theme", "light", "--scale", "1", "--force"]])

    def test_theme_and_scale_pass(self):
        self.runner(0)
        visual.render_png(self.html, self.png, 600, 4200, theme="dark", scale=2)
        self.assertEqual(self.calls[0][-5:], ["--theme", "dark", "--scale", "2", "--force"])

    def test_a_height_not_goes_to_brza_shot(self):
        self.runner(0)
        visual.render_png(self.html, self.png, 736, 4200)
        self.assertNotIn("4200", self.calls[0])

    def test_brza_failure_falls_on_chrome(self):
        self.runner(2, err="boom")
        seen = {}

        def chrome(html, png, width, height, scale):
            seen["args"] = (html, png, width, height, scale)
            open(png, "wb").close()
            return None
        visual._chrome = chrome
        self.assertIsNone(visual.render_png(self.html, self.png, 736, 4200))
        self.assertEqual(seen["args"], (self.html, self.png, 736, 4200, 1))

    def test_css_of_fallback_only_goes_to_chrome_and_the_brza_receives_the_html_intact(self):
        # A14: o `brza shot` injeta os tokens do chat; um `:root` no HTML venceria o tema dele
        self.runner(0)
        self.assertIsNone(visual.render_png(self.html, self.png, 736, chrome_css=":root{--x:1}"))
        self.assertEqual(self.calls[0][2], os.path.abspath(self.html))
        with open(self.html, encoding="utf-8") as f:
            self.assertEqual(f.read(), "<p>oi</p>")
        os.remove(self.png)
        self.runner(2, err="boom")
        seen = {}

        def chrome(html, png, width, height, scale):
            with open(html, encoding="utf-8") as f:
                seen["text"], seen["html"] = f.read(), html
            open(png, "wb").close()
            return None
        visual._chrome = chrome
        self.assertIsNone(visual.render_png(self.html, self.png, 736, chrome_css=":root{--x:1}"))
        self.assertIn("<style>:root{--x:1}</style>", seen["text"])
        self.assertNotEqual(seen["html"], self.html)
        self.assertFalse(os.path.exists(seen["html"]))      # o temporário não fica

    def test_brza_missing_falls_on_chrome_with_a_height_default(self):
        self.runner(127, err="No such file")
        seen = {}
        visual._chrome = lambda h, p, w, a, s: seen.update(height=a) or None
        self.assertIsNone(visual.render_png(self.html, self.png, 736))
        self.assertEqual(seen["height"], visual.CHROME_HEIGHT)

    def test_both_failures_appear_in_the_error(self):
        self.runner(2, err="boom")
        visual._chrome = lambda *a: "Chrome não encontrado; sem PNG"
        error = visual.render_png(self.html, self.png, 736)
        self.assertIn("brza shot falhou (rc 2): boom", error)
        self.assertIn("Chrome não encontrado", error)

    def test_brza_rc0_without_file_also_falls(self):
        self.runner(0, writes=False)
        visual._chrome = lambda *a: "o Chrome não gerou o PNG"
        error = visual.render_png(self.html, self.png, 736)
        self.assertIn("o brza não gerou o PNG", error)

    def test_chrome_real_of_fallback_builds_the_command(self):
        visual.CHROME = __file__  # existe, mas não é o Chrome: o runner trocado vê o comando
        self.runner(0, writes=False)
        visual._run = lambda argv, timeout=60: (self.calls.append(argv), (0, "", ""))[1]
        error = visual._chrome(self.html, self.png, 700, 1500, 1)
        self.assertEqual(error, "o Chrome não gerou o PNG")
        self.assertIn("--window-size=700,1500", self.calls[0])
        self.assertIn("--force-device-scale-factor=1", self.calls[0])
        visual.CHROME = "/nao/existe"
        self.assertIn("não encontrado", visual._chrome(self.html, self.png, 700, 1500, 1))


if __name__ == "__main__":
    unittest.main()
