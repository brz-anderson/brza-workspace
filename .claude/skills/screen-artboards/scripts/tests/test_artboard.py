"""Testes do artboard.py: new (moldura, escopo dos tokens, regras do chat), shot e promote com o `brza shot` trocado."""
import contextlib
import io
import os
import re
import tempfile
import unittest

import _paths  # noqa: F401
import artboard
import tokens

FIX = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
CSS = os.path.join(FIX, 'mini.css')
CSS_DRIFT = os.path.join(FIX, 'mini-deriva.css')
TS = os.path.join(FIX, 'mini-theme.ts')
FRAG = '<style>.tela{height:100%;background:var(--sa-background)}</style><div class="tela">Olá, tela</div>'


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = artboard.main(list(argv))
    return rc, out.getvalue(), err.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.packs = os.path.join(self.dir, 'packs')
        with contextlib.redirect_stdout(io.StringIO()):
            tokens.main(['extract', 'brza-studio', '--src', CSS, '--mobile-src', TS, '--packs-dir', self.packs])
        with open(os.path.join(tokens.PACKS, 'neutral.json'), encoding='utf-8') as f, \
                open(os.path.join(self.packs, 'neutral.json'), 'w', encoding='utf-8') as g:
            g.write(f.read())
        self.body = os.path.join(self.dir, 'tela.html')
        self.writes(self.body, FRAG)
        self.pub = os.path.join(self.dir, 'pub')
        self.saved = os.environ.pop('ORCA_CHAT_SCRATCH_DIR', None)

    def tearDown(self):
        if self.saved is not None:
            os.environ['ORCA_CHAT_SCRATCH_DIR'] = self.saved
        self.tmp.cleanup()

    def writes(self, path, txt):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(txt)

    def fresh(self, slug='tela', frame='macos', *extra, body=None):
        rc, out, err = run('new', slug, '--frame', frame, '--body', body or self.body, '--publish-dir', self.pub,
                            '--packs-dir', self.packs, *extra)
        found = re.search(r'^arquivo: (.*)$', out, re.M)
        doc = ''
        if found:
            with open(found.group(1), encoding='utf-8') as f:
                doc = f.read()
        return rc, out, err, doc


class Rules(unittest.TestCase):
    def failure(self, doc, snippet):
        with self.assertRaises(artboard.RuleError) as cm:
            artboard.check_rules(doc)
        self.assertIn(snippet, str(cm.exception))

    def test_http_outside_of_cdns(self):
        self.failure('<p>x</p>\n<img src="https://exemplo.com/a.png">', 'linha 2')

    def test_cdn_allowed_and_namespace_svg_pass(self):
        artboard.check_rules('<script src="https://cdn.jsdelivr.net/npm/x@1/x.js"></script>'
                                '<svg xmlns="http://www.w3.org/2000/svg"></svg>')

    def test_100vh(self):
        self.failure('<div style="height:100vh"></div>', '100vh')
        self.failure('<div style="min-height: 100 dvh"></div>' .replace('100 dvh', '100dvh'), '100dvh')

    def test_root_redefining_token_of_orca(self):
        self.failure(':root { --background: red; }', ':root')
        self.failure('<style>:root{--primary:#000;--x:1}</style>', '--primary')

    def test_root_with_token_own_passes(self):
        artboard.check_rules(':root { --meu-token: red; } .sa-art { --sa-background: red; }')


class New(Base):
    def test_writes_with_hash_and_prints_a_line(self):
        os.environ['ORCA_CHAT_SCRATCH_DIR'] = self.dir
        rc, out, err, doc = self.fresh('tela', 'macos', '--pack', 'brza-studio', '--letter', 'A', '--title', 'Lista')
        self.assertEqual(rc, 0, err)
        m = re.search(r'::orca-visual\{file="(tela-macos-[0-9a-f]{4}\.html)" title="A — Lista"\}', out)
        self.assertTrue(m, out)
        self.assertTrue(os.path.isfile(os.path.join(self.pub, m.group(1))))

    def test_tokens_scoped_never_on_root(self):
        _, _, _, doc = self.fresh('t', 'browser', '--pack', 'brza-studio', '--scheme', 'both')
        self.assertIn('.sa-art[data-pack="brza-studio"][data-scheme="light"]{', doc)
        self.assertIn('.sa-art[data-pack="brza-studio"][data-scheme="dark"]{', doc)
        self.assertIn('--sa-background:#fff', doc)
        self.assertIn('--sa-background:#0a0a0a', doc)
        self.assertNotRegex(doc, r':root\s*\{')
        artboard.check_rules(doc)

    def test_default_is_both_on_brza_studio_and_light_on_neutral(self):
        _, _, _, d1 = self.fresh('a', 'iphone', '--pack', 'brza-studio')
        _, _, _, d2 = self.fresh('b', 'macos', '--pack', 'neutral')
        self.assertEqual(d1.count('class="sa-cell"'), 2)
        self.assertEqual(d2.count('class="sa-cell"'), 1)

    def test_desktop_of_brza_studio_uses_the_tokens_live_without_scope_of_pack(self):
        for fr in ('macos', 'windows'):
            rc, _, err, doc = self.fresh('v' + fr, fr, '--pack', 'brza-studio')
            self.assertEqual(rc, 0, err)
            self.assertEqual(doc.count('class="sa-cell"'), 1)
            self.assertIn('data-live', doc)
            self.assertNotIn('data-scheme="light"]{', doc)           # nenhum bloco de pacote por esquema
            self.assertNotIn('color-scheme:', doc)
            self.assertIn('--sa-background:var(--background)', doc)
            self.assertIn('--sa-muted-foreground:var(--muted-foreground)', doc)
            self.assertIn('--sa-font-sans:var(--font-sans)', doc)
            self.assertIn('--sa-radius:var(--radius)', doc)
            self.assertIn('--sa-sidebar:var(--muted)', doc)           # o chat não injeta o --sidebar
            self.assertNotIn('--sa-background:#', doc)
            self.assertNotRegex(doc, r':root\s*\{')
            self.assertTrue(artboard.read_meta(doc)['live'])
            artboard.check_rules(doc)

    def test_mobile_browser_and_neutral_continue_scoped(self):
        for fr, pack in (('iphone', 'brza-studio'), ('android', 'brza-studio'), ('browser', 'brza-studio'),
                         ('macos', 'neutral'), ('windows', 'neutral')):
            _, _, _, doc = self.fresh('e' + fr, fr, '--pack', pack, '--scheme', 'light')
            self.assertIn(f'.sa-art[data-pack="{pack}"][data-scheme="light"]{{', doc, (fr, pack))
            self.assertNotIn('data-live', doc, (fr, pack))
            self.assertNotIn('"vivo"', doc)

    def test_explicit_scheme_on_desktop_of_brza_studio_exits_2(self):
        for sch in ('both', 'dark', 'light'):
            rc, _, err, _ = self.fresh('s', 'macos', '--pack', 'brza-studio', '--scheme', sch)
            self.assertEqual(rc, 2)
            self.assertIn('não se aplica ao desktop do brza-studio', err)
        self.assertFalse(os.path.exists(self.pub))

    def test_zoom_inline_by_frame(self):
        _, _, _, doc = self.fresh('t', 'macos', '--pack', 'neutral')
        z = float(re.search(r'style="zoom:([\d.]+);width:1280px"', doc).group(1))
        self.assertAlmostEqual(z, (736 - 24) / 1280, places=3)
        self.assertIn("fr.style.zoom=Math.min(1,f.clientWidth/w)", doc)

    def test_iphone_both_side_by_side_with_zoom_by_half(self):
        _, _, _, doc = self.fresh('m', 'iphone', '--pack', 'brza-studio')
        z = float(re.search(r'zoom:([\d.]+);width:415px', doc).group(1))
        self.assertAlmostEqual(z, ((736 - 24 - 16) / 2) / 415, places=3)
        self.assertEqual(doc.count('class="sa-row"'), 1)

    def test_mobile_uses_the_mobile_value_where_there_is_a_pair(self):
        _, _, _, mob = self.fresh('m', 'iphone', '--pack', 'brza-studio', '--scheme', 'light')
        _, _, _, desktop_css = self.fresh('d', 'browser', '--pack', 'brza-studio', '--scheme', 'light')
        self.assertIn('--sa-sidebar:#fafafa', desktop_css)
        self.assertIn('--sa-border:#e5e5e5', mob)
        _, _, _, mobile_dark = self.fresh('md', 'iphone', '--pack', 'brza-studio', '--scheme', 'dark')
        self.assertIn('--sa-border:rgba(255, 255, 255, 0.07)', mobile_dark)   # o do mobile, por cima do rgb() do desktop

    def test_browser_stacks_the_three_widths(self):
        _, _, _, doc = self.fresh('w', 'browser', '--pack', 'neutral', '--url', 'x.com/a', '--window-title', 'Radar')
        self.assertEqual(re.findall(r'data-w="(\d+)" data-scheme', doc), ['375', '768', '1280'])
        self.assertEqual(doc.count('class="sa-row"'), 3)
        self.assertIn('x.com/a', doc)
        self.assertEqual(artboard.read_meta(doc)['widths'], [375, 768, 1280])

    def test_browser_widths_and_widths_in_other_frame(self):
        _, _, _, doc = self.fresh('w', 'browser', '--pack', 'neutral', '--widths', '375,1280')
        self.assertEqual(artboard.read_meta(doc)['widths'], [375, 1280])
        rc, _, err, _ = self.fresh('x', 'macos', '--widths', '375')
        self.assertEqual(rc, 2)

    def test_refuses_fragment_with_rule_broken(self):
        bad = os.path.join(self.dir, 'ruim.html')
        self.writes(bad, '<div style="height:100vh">x</div>')
        rc, _, err, _ = self.fresh('r', 'macos', body=bad)
        self.assertEqual(rc, 1)
        self.assertIn('100vh', err)
        self.assertFalse(os.path.exists(self.pub))

    def test_refuses_html_of_512kb(self):
        large = os.path.join(self.dir, 'grande.html')
        self.writes(large, '<p>' + 'x' * (512 * 1024) + '</p>')
        rc, _, err, _ = self.fresh('g', 'macos', body=large)
        self.assertEqual(rc, 1)
        self.assertIn('512 KB', err)

    def test_name_new_when_the_content_changes(self):
        _, o1, _, _ = self.fresh('t', 'macos', '--pack', 'neutral')
        self.writes(self.body, FRAG + '<!-- v2 -->')
        _, o2, _, _ = self.fresh('t', 'macos', '--pack', 'neutral')
        self.assertNotEqual(re.search(r'arquivo: .*', o1).group(0), re.search(r'arquivo: .*', o2).group(0))

    def test_pack_missing_exits_2(self):
        rc, _, err, _ = self.fresh('t', 'macos', '--pack', 'nao-existe')
        self.assertEqual(rc, 2)

    def test_drift_only_warns(self):
        # o pacote foi extraído do CSS e do TS de fixture; aponta a origem para o CSS que mudou
        p = os.path.join(self.packs, 'brza-studio.json')
        with open(p, encoding='utf-8') as f:
            txt = f.read().replace(CSS, CSS_DRIFT)
        self.writes(p, txt)
        rc, out, err, doc = self.fresh('t', 'macos', '--pack', 'brza-studio')
        self.assertEqual(rc, 0)
        self.assertIn('deriva', err)
        self.assertTrue(doc)

    def test_without_scratch_of_chat_not_prints_a_line(self):
        rc, out, err = run('new', 't', '--frame', 'macos', '--pack', 'neutral', '--body', self.body,
                            '--packs-dir', self.packs, '--publish-dir', '')
        self.assertEqual(rc, 0, err)
        self.assertNotIn('::orca-visual', out)
        self.assertIn('fora do chat', out)

    def test_the_fragment_goes_inside_of_screen_and_the_five_frames_exist(self):
        for fr in sorted(artboard.FRAMES):
            _, _, _, doc = self.fresh('f', fr, '--pack', 'neutral')
            self.assertIn('Olá, tela', doc, fr)
            self.assertIn(f'sa-{fr}', doc, fr)
            self.assertNotIn('{{', doc, fr)


class Png(Base):
    def setUp(self):
        super().setUp()
        self.calls = []
        self.orig = artboard.render_png

        def fake_value(html, png, width, height=None, *, theme='light', scale=1, chrome_css=''):
            self.calls.append({'html': html, 'png': png, 'w': width, 'theme': theme, 'scale': scale, 'css': chrome_css})
            with open(png, 'wb') as f:
                f.write(b'png')
            return None
        artboard.render_png = fake_value

    def tearDown(self):
        artboard.render_png = self.orig
        super().tearDown()

    def artboard(self, frame, *extra):
        _, out, _, _ = self.fresh('t', frame, '--pack', 'brza-studio', *extra)
        return re.search(r'^arquivo: (.*)$', out, re.M).group(1)

    def test_shot_one_png_by_width_and_theme_and_one_a_736(self):
        a = self.artboard('browser', '--scheme', 'both', '--widths', '1280')
        out_dir = os.path.join(self.dir, 'png')
        rc, out, _ = run('shot', a, '--out-dir', out_dir)
        self.assertEqual(rc, 0)
        name_list = [os.path.basename(x) for x in out.split()]
        base = os.path.splitext(os.path.basename(a))[0]
        self.assertEqual(name_list, [f'{base}-736.png', f'{base}-1280-light.png', f'{base}-1280-dark.png'])
        self.assertEqual([c['w'] for c in self.calls], [736, 1280 + 24, 1280 + 24])
        self.assertEqual([c['theme'] for c in self.calls], ['light', 'light', 'dark'])

    def test_shot_of_pre_rename_meta_asks_to_regenerate(self):
        path = os.path.join(self.dir, 'old.html')
        self.writes(path, '<meta name="sa-art" content="{&quot;esquemas&quot;:[&quot;light&quot;],&quot;larguras&quot;:[1280]}">')
        rc, out, err = run('shot', path, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual(rc, 1)
        self.assertIn('regere o artboard', err)
        self.assertNotIn('Traceback', out + err)

    def test_shot_desktop_of_brza_studio_injects_the_fallback_only_on_the_png(self):
        a = self.artboard('macos')
        with open(a, encoding='utf-8') as f:
            self.assertNotRegex(f.read(), r':root\s*\{')            # o artboard publicado não leva o fallback
        out_dir = os.path.join(self.dir, 'png')
        rc, out, _ = run('shot', a, '--out-dir', out_dir, '--packs-dir', self.packs)
        self.assertEqual(rc, 0)
        base = os.path.splitext(os.path.basename(a))[0]
        self.assertEqual([os.path.basename(x) for x in out.split()], [f'{base}-736.png', f'{base}-1280-light.png'])
        self.assertEqual([c['w'] for c in self.calls], [736, 1304])
        for c in self.calls:
            # A14: o HTML que o `brza shot` abre não leva o `:root` (venceria os tokens que ele injeta); o CSS de reserva
            # vai à parte, só para o Chrome
            with open(c['html'], encoding='utf-8') as f:
                self.assertNotIn(':root{', f.read())
            self.assertIn(':root{color-scheme:light;--', c['css'])
            self.assertIn('--background:#fff', c['css'])
            self.assertIn('--font-sans:', c['css'])

    def test_shot_desktop_of_brza_studio_with_theme_dark(self):
        a = self.artboard('windows')
        run('shot', a, '--out-dir', os.path.join(self.dir, 'png'), '--theme', 'dark', '--packs-dir', self.packs)
        self.assertEqual([c['theme'] for c in self.calls], ['dark', 'dark'])
        for c in self.calls:
            with open(c['html'], encoding='utf-8') as f:
                self.assertNotIn(':root{', f.read())
            self.assertIn(':root{color-scheme:dark;', c['css'])
            self.assertIn('--background:#0a0a0a', c['css'])

    def test_shot_mobile_and_neutral_not_inject_fallback(self):
        a = self.artboard('iphone', '--scheme', 'dark')
        run('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        with open(self.calls[1]['html'], encoding='utf-8') as f:
            self.assertNotIn(':root{', f.read())
        self.assertEqual([c['css'] for c in self.calls], ['', ''])

    def test_promote_desktop_of_brza_studio_with_theme(self):
        root = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(root, 'plans', 'PLN-099-x'))
        a = self.artboard('macos')
        rc, _, err = run('promote', a, '--plan', '99', '--name', 'esc', '--scheme', 'dark', '--root', root,
                          '--packs-dir', self.packs)
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.calls[0]['theme'], 'dark')
        self.assertIn('--background:#0a0a0a', self.calls[0]['css'])
        with open(self.calls[0]['html'], encoding='utf-8') as f:
            self.assertNotIn(':root{', f.read())

    def test_shot_web_one_variant_by_width(self):
        _, out, _, _ = self.fresh('w', 'browser', '--pack', 'neutral')
        a = re.search(r'^arquivo: (.*)$', out, re.M).group(1)
        rc, out, _ = run('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual(rc, 0)
        self.assertEqual([c['w'] for c in self.calls], [736, 375 + 24, 768 + 24, 1280 + 24])
        # cada variante esconde as outras molduras
        with open(self.calls[2]['html'], encoding='utf-8') as f:
            var = f.read()
        self.assertIn('.sa-cell:not([data-w="768"][data-scheme="light"]){display:none}', var)

    def test_shot_iphone_uses_a_width_outer_of_device(self):
        a = self.artboard('iphone', '--scheme', 'dark')
        run('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual([c['w'] for c in self.calls], [736, 415 + 24])

    def test_shot_with_theme_only_strips_that_scheme(self):
        a = self.artboard('browser', '--scheme', 'both', '--widths', '1280')
        run('shot', a, '--out-dir', os.path.join(self.dir, 'png'), '--theme', 'dark')
        self.assertEqual([c['theme'] for c in self.calls], ['dark'] * 2)

    def test_shot_error_of_png_exits_1(self):
        artboard.render_png = lambda *a, **k: 'brza shot falhou'
        a = self.artboard('macos')
        rc, _, err = run('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual(rc, 1)
        self.assertIn('brza shot falhou', err)

    def test_shot_of_file_that_is_not_artboard(self):
        x = os.path.join(self.dir, 'x.html')
        self.writes(x, '<p>oi</p>')
        self.assertEqual(run('shot', x, '--out-dir', self.dir)[0], 1)

    def test_promote_plan(self):
        root = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(root, 'plans', 'PLN-099-um-plano'))
        a = self.artboard('macos')
        rc, out, err = run('promote', a, '--plan', 'PLN-099', '--name', 'Lista de Chats', '--root', root)
        self.assertEqual(rc, 0, err)
        png = os.path.join(root, 'plans', 'PLN-099-um-plano', 'PLN-099-lista-de-chats.png')
        self.assertTrue(os.path.isfile(png))
        self.assertIn('![lista de chats](PLN-099-lista-de-chats.png)', out)
        self.assertEqual(self.calls[0]['w'], 1304)
        self.assertEqual(self.calls[0]['scale'], 2)

    def test_promote_chooses_width_and_scheme(self):
        root = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(root, 'plans', 'PLN-099-x'))
        _, out, _, _ = self.fresh('w', 'browser', '--pack', 'brza-studio')
        a = re.search(r'^arquivo: (.*)$', out, re.M).group(1)
        rc, _, _ = run('promote', a, '--plan', '99', '--name', 'tablet', '--width', '768', '--scheme', 'dark',
                        '--root', root)
        self.assertEqual(rc, 0)
        self.assertEqual((self.calls[0]['w'], self.calls[0]['theme']), (768 + 24, 'dark'))
        self.assertEqual(run('promote', a, '--plan', '99', '--name', 'x', '--width', '999', '--root', root)[0], 2)

    def test_promote_issue_writes_to_side(self):
        root = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(root, 'work', 'issues'))
        self.writes(os.path.join(root, 'work', 'issues', 'ISS-001-tela.md'), '# x\n')
        a = self.artboard('macos')
        rc, out, err = run('promote', a, '--issue', 'work/issues/ISS-001-tela.md', '--name', 'v1', '--root', root)
        self.assertEqual(rc, 0, err)
        self.assertTrue(os.path.isfile(os.path.join(root, 'work', 'issues', 'ISS-001-tela-v1.png')))

    def test_promote_without_a_folder_of_plan_exits_1(self):
        a = self.artboard('macos')
        rc, _, err = run('promote', a, '--plan', 'PLN-077', '--name', 'x', '--root', self.dir)
        self.assertEqual(rc, 1)
        self.assertIn('PLN-077', err)


class OutputCase(unittest.TestCase):
    def test_folder_of_output(self):
        self.assertEqual(artboard.output_dir('/x'), ('/x', True))
        os.environ.pop('ORCA_CHAT_SCRATCH_DIR', None)
        self.assertFalse(artboard.output_dir(None)[1])


if __name__ == '__main__':
    unittest.main()
