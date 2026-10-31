"""Testes do brza-shot: o tema lido do main.css, o shell lido do código do brza-studio, a recusa do destino e, quando a
máquina tem o Chrome, a captura de um brza-studio de mentira nos dois temas.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import io
import os
import runpy
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).parent.parent
SHOT = runpy.run_path(str(SCRIPTS / 'brza-shot'))
ShotError = SHOT['ShotError']
CHROME = Path(os.environ.get('BRZA_CHROME') or SHOT['CHROME'])

MAIN_CSS = '''@import 'tailwindcss';
/* :root { --background: errado; } */
@theme inline { --color-background: var(--background); }
:root {
  --background: #ff0000;
  --foreground: #111;
  --font-sans: var(--app-font);
  --app-font: 'Geist', sans-serif;
  --chart-1: var(--color-blue-300);
}
.dark {
  --background: #0000ff;
}
:root,
.native-chat-appearance[data-native-chat-scheme='light'] {
  --destructive: #e40014;
}
.dark,
.native-chat-appearance[data-native-chat-scheme='dark'] {
  --destructive: #ff6568;
}
.plugin-security-chrome { --background: #00ff00; }
@layer base { :root { --background: #abcdef; } }
'''
TAILWIND = '@theme default {\n  --color-blue-300: oklch(80.9% 0.105 251.813);\n}\n'
PANEL = """export const PANEL_DESIGN_TOKEN_ALLOWLIST = [
  '--background',
  '--foreground',
  '--destructive'
] as const
"""
VISUAL = """export const NATIVE_CHAT_VISUAL_CDN_ORIGINS = [
  'https://cdn.jsdelivr.net',
  'https://unpkg.com'
] as const
export const NATIVE_CHAT_VISUAL_THEME_TOKENS = [
  ...PANEL_DESIGN_TOKEN_ALLOWLIST,
  '--chart-1',
  '--font-sans'
] as const
const BASE_CSS =
  'html{background:var(--background);color:var(--foreground);' +
  'font-size:14px}body{margin:0}'
"""


def fake_studio(root: Path, tailwind: bool = True) -> Path:
    files = {SHOT['MAIN_CSS']: MAIN_CSS, SHOT['PANEL_SHELL']: PANEL, SHOT['VISUAL_SHELL']: VISUAL}
    if tailwind:
        files[SHOT['TAILWIND_THEME']] = TAILWIND
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    return root


def first_pixel(png: bytes) -> tuple[int, int, int]:
    """O RGB do pixel do canto: no primeiro pixel da primeira linha, todo filtro do PNG devolve o byte cru."""
    color_type, chunks, i = png[25], b'', 8
    while i < len(png):
        size, kind = int.from_bytes(png[i:i + 4], 'big'), png[i + 4:i + 8]
        if kind == b'IDAT':
            chunks += png[i + 8:i + 8 + size]
        i += 12 + size
    assert color_type in (2, 6), color_type
    raw = zlib.decompress(chunks)
    return raw[1], raw[2], raw[3]


class ThemeTest(unittest.TestCase):
    def test_dark_overrides_root_in_file_order_and_other_selectors_stay_out(self):
        light = SHOT['theme_variables'](MAIN_CSS, TAILWIND, 'light')
        dark = SHOT['theme_variables'](MAIN_CSS, TAILWIND, 'dark')
        self.assertEqual((light['--background'], light['--destructive']), ('#ff0000', '#e40014'))
        self.assertEqual((dark['--background'], dark['--destructive']), ('#0000ff', '#ff6568'))
        self.assertEqual(dark['--foreground'], '#111')
        self.assertEqual(light['--color-blue-300'], 'oklch(80.9% 0.105 251.813)')

    def test_multiline_values_collapse_into_one_line(self):
        css = ':root {\n  --chat-canvas: color-mix(\n    in srgb,\n    var(--a) 5%,\n    var(--b)\n  );\n}\n'
        self.assertEqual(SHOT['theme_variables'](css, '', 'light')['--chat-canvas'],
                         'color-mix(in srgb, var(--a) 5%, var(--b))')

    def test_resolve_follows_vars_fallbacks_and_drops_the_undefined(self):
        resolve = SHOT['resolve']
        variables = {'--a': 'var(--b)', '--b': '#fff', '--loop': 'var(--loop)'}
        self.assertEqual(resolve('color-mix(in srgb, var(--a) 5%, var(--b))', variables),
                         'color-mix(in srgb, #fff 5%, #fff)')
        self.assertEqual(resolve('var(--nada, var(--b))', variables), '#fff')
        self.assertEqual(resolve('var(--nada, 1px solid)', variables), '1px solid')
        self.assertIsNone(resolve('var(--nada)', variables))
        self.assertIsNone(resolve('var(--loop)', variables))

    def test_scoped_tokens_read_the_chat_scope_first(self):
        variables = {'--chat-canvas': 'var(--background)', '--background': '#000', '--foreground': '#eee'}
        tokens = SHOT['theme_tokens'](variables, ['--background', '--foreground', '--ring'])
        self.assertEqual(tokens, {'--background': '#000', '--foreground': '#eee'})

    def test_studio_theme_reads_the_tokens_and_warns_without_tailwind(self):
        with tempfile.TemporaryDirectory() as tmp:
            tokens, parts, warnings = SHOT['studio_theme'](fake_studio(Path(tmp)), 'dark')
            self.assertEqual(tokens['--background'], '#0000ff')
            self.assertEqual(tokens['--chart-1'], 'oklch(80.9% 0.105 251.813)')
            self.assertEqual(tokens['--font-sans'], "'Geist', sans-serif")
            self.assertEqual(warnings, [])
        with tempfile.TemporaryDirectory() as tmp:
            tokens, _, warnings = SHOT['studio_theme'](fake_studio(Path(tmp), tailwind=False), 'light')
            self.assertNotIn('--chart-1', tokens)
            self.assertIn('pnpm install', warnings[0])
            self.assertIn('--chart-1', warnings[1])


class ShellTest(unittest.TestCase):
    def test_parts_come_from_the_studio_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            parts = SHOT['shell_parts'](fake_studio(Path(tmp)))
        self.assertEqual(parts['tokens'], ['--background', '--foreground', '--destructive', '--chart-1', '--font-sans'])
        self.assertEqual(parts['cdns'], ['https://cdn.jsdelivr.net', 'https://unpkg.com'])
        self.assertEqual(parts['base_css'],
                         'html{background:var(--background);color:var(--foreground);font-size:14px}body{margin:0}')

    def test_changed_studio_code_stops_with_the_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            studio = fake_studio(Path(tmp))
            (studio / SHOT['VISUAL_SHELL']).write_text(VISUAL.replace('BASE_CSS', 'SHELL_CSS'))
            with self.assertRaisesRegex(ShotError, 'BASE_CSS'):
                SHOT['shell_parts'](studio)

    def test_theme_css_strips_what_closes_the_style(self):
        css = SHOT['theme_css']('dark', {'--a': '#fff', '--b': 'x}</style><script>', '--C': '#000', '--d': ';'})
        self.assertEqual(css, ':root{color-scheme:dark;--a:#fff;--b:x/stylescript}')

    def test_document_puts_the_artboard_after_the_head(self):
        parts = {'cdns': ['https://unpkg.com'], 'base_css': 'body{margin:0}'}
        doc = SHOT['build_document']('<body>oi</body>', 'light', {'--background': '#fff'}, parts)
        self.assertTrue(doc.startswith('<!doctype html>\n<html class="light">'))
        self.assertIn("script-src 'unsafe-inline' data: blob: https://unpkg.com", doc)
        self.assertIn("connect-src 'none'", doc)
        self.assertIn('<style id="orca-visual-theme">:root{color-scheme:light;--background:#fff}</style>', doc)
        self.assertTrue(doc.endswith('</head>\n<body>oi</body>'))


class MainTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.source = self.base / 'a.html'
        self.source.write_text('<body>oi</body>')

    def run_main(self, *args) -> tuple[int, str]:
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()), \
                patch.dict(os.environ, {'BRZA_CHROME': str(self.source)}):
            try:
                SHOT['main']([str(a) for a in args])
            except SystemExit as e:
                return e.code, err.getvalue()
        return 0, err.getvalue()

    def test_existing_destination_is_refused_without_force(self):
        dest = self.base / 'a.png'
        dest.write_bytes(b'antigo')
        code, err = self.run_main(self.source, dest)
        self.assertEqual(code, 2)
        self.assertIn('já existe; use --force', err)
        self.assertEqual(dest.read_bytes(), b'antigo')

    def test_force_goes_through_to_the_capture(self):
        dest = self.base / 'a.png'
        dest.write_bytes(b'antigo')
        calls = []
        with patch.dict(SHOT['main'].__globals__, shot=lambda *a: calls.append(a) or ((10, 20), [])):
            code, _ = self.run_main(self.source, dest, '--force', '--theme', 'dark', '--width', '640')
        self.assertEqual(code, 0)
        self.assertEqual(calls[0][2:5], ('dark', 640, 2))

    def test_bad_arguments_are_refused(self):
        cases = [
            ((self.base / 'nada.html', self.base / 'a.png'), 'não existe'),
            ((self.source, self.base / 'a.jpg'), 'não termina em .png'),
            ((self.source, self.base / 'sem' / 'a.png'), 'não existe'),
            ((self.source, self.base / 'a.png', '--width', '0'), 'positivos'),
        ]
        for args, message in cases:
            code, err = self.run_main(*args)
            self.assertEqual(code, 2, args)
            self.assertIn(message, err, args)


@unittest.skipUnless(CHROME.exists(), f'sem o Chrome em {CHROME}')
class CaptureTest(unittest.TestCase):
    def test_captures_the_whole_page_in_both_themes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            studio = fake_studio(base / 'studio')
            source = base / 'a.html'
            source.write_text('<body><div style="height:1500px"></div></body>')
            for scheme, color in (('light', (255, 0, 0)), ('dark', (0, 0, 255))):
                dest = base / f'{scheme}.png'
                size, warnings = SHOT['shot'](source, dest, scheme, 400, 1, 0, studio, CHROME)
                self.assertEqual(size, (400, 1500))
                self.assertEqual(warnings, [])
                self.assertEqual(first_pixel(dest.read_bytes()), color)


if __name__ == '__main__':
    unittest.main()
