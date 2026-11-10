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
CSS_DERIVA = os.path.join(FIX, 'mini-deriva.css')
TS = os.path.join(FIX, 'mini-theme.ts')
FRAG = '<style>.tela{height:100%;background:var(--sa-background)}</style><div class="tela">Olá, tela</div>'


def roda(*argv):
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
        self.escreve(self.body, FRAG)
        self.pub = os.path.join(self.dir, 'pub')
        self.salvo = os.environ.pop('ORCA_CHAT_SCRATCH_DIR', None)

    def tearDown(self):
        if self.salvo is not None:
            os.environ['ORCA_CHAT_SCRATCH_DIR'] = self.salvo
        self.tmp.cleanup()

    def escreve(self, caminho, txt):
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(txt)

    def novo(self, slug='tela', frame='macos', *extra, body=None):
        rc, out, err = roda('new', slug, '--frame', frame, '--body', body or self.body, '--publish-dir', self.pub,
                            '--packs-dir', self.packs, *extra)
        arq = re.search(r'^arquivo: (.*)$', out, re.M)
        doc = ''
        if arq:
            with open(arq.group(1), encoding='utf-8') as f:
                doc = f.read()
        return rc, out, err, doc


class Regras(unittest.TestCase):
    def falha(self, doc, trecho):
        with self.assertRaises(artboard.ErroRegra) as cm:
            artboard.confere_regras(doc)
        self.assertIn(trecho, str(cm.exception))

    def test_http_fora_dos_cdns(self):
        self.falha('<p>x</p>\n<img src="https://exemplo.com/a.png">', 'linha 2')

    def test_cdn_permitido_e_namespace_svg_passam(self):
        artboard.confere_regras('<script src="https://cdn.jsdelivr.net/npm/x@1/x.js"></script>'
                                '<svg xmlns="http://www.w3.org/2000/svg"></svg>')

    def test_100vh(self):
        self.falha('<div style="height:100vh"></div>', '100vh')
        self.falha('<div style="min-height: 100 dvh"></div>' .replace('100 dvh', '100dvh'), '100dvh')

    def test_root_redefinindo_token_do_orca(self):
        self.falha(':root { --background: red; }', ':root')
        self.falha('<style>:root{--primary:#000;--x:1}</style>', '--primary')

    def test_root_com_token_proprio_passa(self):
        artboard.confere_regras(':root { --meu-token: red; } .sa-art { --sa-background: red; }')


class New(Base):
    def test_grava_com_hash_e_imprime_a_linha(self):
        os.environ['ORCA_CHAT_SCRATCH_DIR'] = self.dir
        rc, out, err, doc = self.novo('tela', 'macos', '--pack', 'brza-studio', '--letter', 'A', '--title', 'Lista')
        self.assertEqual(rc, 0, err)
        m = re.search(r'::orca-visual\{file="(tela-macos-[0-9a-f]{4}\.html)" title="A — Lista"\}', out)
        self.assertTrue(m, out)
        self.assertTrue(os.path.isfile(os.path.join(self.pub, m.group(1))))

    def test_tokens_escopados_nunca_no_root(self):
        _, _, _, doc = self.novo('t', 'browser', '--pack', 'brza-studio', '--scheme', 'both')
        self.assertIn('.sa-art[data-pack="brza-studio"][data-scheme="light"]{', doc)
        self.assertIn('.sa-art[data-pack="brza-studio"][data-scheme="dark"]{', doc)
        self.assertIn('--sa-background:#fff', doc)
        self.assertIn('--sa-background:#0a0a0a', doc)
        self.assertNotRegex(doc, r':root\s*\{')
        artboard.confere_regras(doc)

    def test_padrao_both_no_brza_studio_e_light_no_neutro(self):
        _, _, _, d1 = self.novo('a', 'iphone', '--pack', 'brza-studio')
        _, _, _, d2 = self.novo('b', 'macos', '--pack', 'neutral')
        self.assertEqual(d1.count('class="sa-cell"'), 2)
        self.assertEqual(d2.count('class="sa-cell"'), 1)

    def test_desktop_do_brza_studio_usa_os_tokens_vivos_sem_escopo_de_pacote(self):
        for fr in ('macos', 'windows'):
            rc, _, err, doc = self.novo('v' + fr, fr, '--pack', 'brza-studio')
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
            self.assertTrue(artboard.le_meta(doc)['vivo'])
            artboard.confere_regras(doc)

    def test_mobile_browser_e_neutral_seguem_escopados(self):
        for fr, pack in (('iphone', 'brza-studio'), ('android', 'brza-studio'), ('browser', 'brza-studio'),
                         ('macos', 'neutral'), ('windows', 'neutral')):
            _, _, _, doc = self.novo('e' + fr, fr, '--pack', pack, '--scheme', 'light')
            self.assertIn(f'.sa-art[data-pack="{pack}"][data-scheme="light"]{{', doc, (fr, pack))
            self.assertNotIn('data-live', doc, (fr, pack))
            self.assertNotIn('"vivo"', doc)

    def test_scheme_explicito_no_desktop_do_brza_studio_sai_2(self):
        for sch in ('both', 'dark', 'light'):
            rc, _, err, _ = self.novo('s', 'macos', '--pack', 'brza-studio', '--scheme', sch)
            self.assertEqual(rc, 2)
            self.assertIn('não se aplica ao desktop do brza-studio', err)
        self.assertFalse(os.path.exists(self.pub))

    def test_zoom_inline_por_moldura(self):
        _, _, _, doc = self.novo('t', 'macos', '--pack', 'neutral')
        z = float(re.search(r'style="zoom:([\d.]+);width:1280px"', doc).group(1))
        self.assertAlmostEqual(z, (736 - 24) / 1280, places=3)
        self.assertIn("fr.style.zoom=Math.min(1,f.clientWidth/w)", doc)

    def test_iphone_both_lado_a_lado_com_zoom_pela_metade(self):
        _, _, _, doc = self.novo('m', 'iphone', '--pack', 'brza-studio')
        z = float(re.search(r'zoom:([\d.]+);width:415px', doc).group(1))
        self.assertAlmostEqual(z, ((736 - 24 - 16) / 2) / 415, places=3)
        self.assertEqual(doc.count('class="sa-row"'), 1)

    def test_mobile_usa_o_valor_do_mobile_onde_ha_par(self):
        _, _, _, mob = self.novo('m', 'iphone', '--pack', 'brza-studio', '--scheme', 'light')
        _, _, _, des = self.novo('d', 'browser', '--pack', 'brza-studio', '--scheme', 'light')
        self.assertIn('--sa-sidebar:#fafafa', des)
        self.assertIn('--sa-border:#e5e5e5', mob)
        _, _, _, mob_d = self.novo('md', 'iphone', '--pack', 'brza-studio', '--scheme', 'dark')
        self.assertIn('--sa-border:rgba(255, 255, 255, 0.07)', mob_d)   # o do mobile, por cima do rgb() do desktop

    def test_browser_empilha_as_tres_larguras(self):
        _, _, _, doc = self.novo('w', 'browser', '--pack', 'neutral', '--url', 'x.com/a', '--window-title', 'Radar')
        self.assertEqual(re.findall(r'data-w="(\d+)" data-scheme', doc), ['375', '768', '1280'])
        self.assertEqual(doc.count('class="sa-row"'), 3)
        self.assertIn('x.com/a', doc)
        self.assertEqual(artboard.le_meta(doc)['larguras'], [375, 768, 1280])

    def test_browser_widths_e_widths_em_outra_moldura(self):
        _, _, _, doc = self.novo('w', 'browser', '--pack', 'neutral', '--widths', '375,1280')
        self.assertEqual(artboard.le_meta(doc)['larguras'], [375, 1280])
        rc, _, err, _ = self.novo('x', 'macos', '--widths', '375')
        self.assertEqual(rc, 2)

    def test_recusa_fragmento_com_regra_quebrada(self):
        ruim = os.path.join(self.dir, 'ruim.html')
        self.escreve(ruim, '<div style="height:100vh">x</div>')
        rc, _, err, _ = self.novo('r', 'macos', body=ruim)
        self.assertEqual(rc, 1)
        self.assertIn('100vh', err)
        self.assertFalse(os.path.exists(self.pub))

    def test_recusa_html_de_512kb(self):
        grande = os.path.join(self.dir, 'grande.html')
        self.escreve(grande, '<p>' + 'x' * (512 * 1024) + '</p>')
        rc, _, err, _ = self.novo('g', 'macos', body=grande)
        self.assertEqual(rc, 1)
        self.assertIn('512 KB', err)

    def test_nome_novo_quando_o_conteudo_muda(self):
        _, o1, _, _ = self.novo('t', 'macos', '--pack', 'neutral')
        self.escreve(self.body, FRAG + '<!-- v2 -->')
        _, o2, _, _ = self.novo('t', 'macos', '--pack', 'neutral')
        self.assertNotEqual(re.search(r'arquivo: .*', o1).group(0), re.search(r'arquivo: .*', o2).group(0))

    def test_pacote_inexistente_sai_2(self):
        rc, _, err, _ = self.novo('t', 'macos', '--pack', 'nao-existe')
        self.assertEqual(rc, 2)

    def test_deriva_so_avisa(self):
        # o pacote foi extraído do CSS e do TS de fixture; aponta a origem para o CSS que mudou
        p = os.path.join(self.packs, 'brza-studio.json')
        with open(p, encoding='utf-8') as f:
            txt = f.read().replace(CSS, CSS_DERIVA)
        self.escreve(p, txt)
        rc, out, err, doc = self.novo('t', 'macos', '--pack', 'brza-studio')
        self.assertEqual(rc, 0)
        self.assertIn('deriva', err)
        self.assertTrue(doc)

    def test_sem_scratch_do_chat_nao_imprime_a_linha(self):
        rc, out, err = roda('new', 't', '--frame', 'macos', '--pack', 'neutral', '--body', self.body,
                            '--packs-dir', self.packs, '--publish-dir', '')
        self.assertEqual(rc, 0, err)
        self.assertNotIn('::orca-visual', out)
        self.assertIn('fora do chat', out)

    def test_o_fragmento_vai_dentro_da_tela_e_as_cinco_molduras_existem(self):
        for fr in sorted(artboard.FRAMES):
            _, _, _, doc = self.novo('f', fr, '--pack', 'neutral')
            self.assertIn('Olá, tela', doc, fr)
            self.assertIn(f'sa-{fr}', doc, fr)
            self.assertNotIn('{{', doc, fr)


class Png(Base):
    def setUp(self):
        super().setUp()
        self.chamadas = []
        self.orig = artboard.gera_png

        def falso(html, png, width, altura=None, *, theme='light', scale=1):
            self.chamadas.append({'html': html, 'png': png, 'w': width, 'theme': theme, 'scale': scale})
            with open(png, 'wb') as f:
                f.write(b'png')
            return None
        artboard.gera_png = falso

    def tearDown(self):
        artboard.gera_png = self.orig
        super().tearDown()

    def artboard(self, frame, *extra):
        _, out, _, _ = self.novo('t', frame, '--pack', 'brza-studio', *extra)
        return re.search(r'^arquivo: (.*)$', out, re.M).group(1)

    def test_shot_um_png_por_largura_e_tema_e_um_a_736(self):
        a = self.artboard('browser', '--scheme', 'both', '--widths', '1280')
        out_dir = os.path.join(self.dir, 'png')
        rc, out, _ = roda('shot', a, '--out-dir', out_dir)
        self.assertEqual(rc, 0)
        nomes = [os.path.basename(x) for x in out.split()]
        base = os.path.splitext(os.path.basename(a))[0]
        self.assertEqual(nomes, [f'{base}-736.png', f'{base}-1280-light.png', f'{base}-1280-dark.png'])
        self.assertEqual([c['w'] for c in self.chamadas], [736, 1280 + 24, 1280 + 24])
        self.assertEqual([c['theme'] for c in self.chamadas], ['light', 'light', 'dark'])

    def test_shot_desktop_do_brza_studio_injeta_o_fallback_so_no_png(self):
        a = self.artboard('macos')
        with open(a, encoding='utf-8') as f:
            self.assertNotRegex(f.read(), r':root\s*\{')            # o artboard publicado não leva o fallback
        out_dir = os.path.join(self.dir, 'png')
        rc, out, _ = roda('shot', a, '--out-dir', out_dir, '--packs-dir', self.packs)
        self.assertEqual(rc, 0)
        base = os.path.splitext(os.path.basename(a))[0]
        self.assertEqual([os.path.basename(x) for x in out.split()], [f'{base}-736.png', f'{base}-1280-light.png'])
        self.assertEqual([c['w'] for c in self.chamadas], [736, 1304])
        for c in self.chamadas:
            with open(c['html'], encoding='utf-8') as f:
                var = f.read()
            self.assertIn(':root{color-scheme:light;--', var)
            self.assertIn('--background:#fff', var)
            self.assertIn('--font-sans:', var)
            self.assertNotEqual(c['html'], a)

    def test_shot_desktop_do_brza_studio_com_theme_dark(self):
        a = self.artboard('windows')
        roda('shot', a, '--out-dir', os.path.join(self.dir, 'png'), '--theme', 'dark', '--packs-dir', self.packs)
        self.assertEqual([c['theme'] for c in self.chamadas], ['dark', 'dark'])
        for c in self.chamadas:
            with open(c['html'], encoding='utf-8') as f:
                var = f.read()
            self.assertIn(':root{color-scheme:dark;', var)
            self.assertIn('--background:#0a0a0a', var)

    def test_shot_mobile_e_neutral_nao_injetam_fallback(self):
        a = self.artboard('iphone', '--scheme', 'dark')
        roda('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        with open(self.chamadas[1]['html'], encoding='utf-8') as f:
            self.assertNotIn(':root{', f.read())

    def test_promote_desktop_do_brza_studio_com_tema(self):
        raiz = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(raiz, 'plans', 'PLN-099-x'))
        a = self.artboard('macos')
        rc, _, err = roda('promote', a, '--plan', '99', '--name', 'esc', '--scheme', 'dark', '--root', raiz,
                          '--packs-dir', self.packs)
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.chamadas[0]['theme'], 'dark')
        with open(self.chamadas[0]['html'], encoding='utf-8') as f:
            self.assertIn('--background:#0a0a0a', f.read())

    def test_shot_web_uma_variante_por_largura(self):
        _, out, _, _ = self.novo('w', 'browser', '--pack', 'neutral')
        a = re.search(r'^arquivo: (.*)$', out, re.M).group(1)
        rc, out, _ = roda('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual(rc, 0)
        self.assertEqual([c['w'] for c in self.chamadas], [736, 375 + 24, 768 + 24, 1280 + 24])
        # cada variante esconde as outras molduras
        with open(self.chamadas[2]['html'], encoding='utf-8') as f:
            var = f.read()
        self.assertIn('.sa-cell:not([data-w="768"][data-scheme="light"]){display:none}', var)

    def test_shot_iphone_usa_a_largura_externa_do_aparelho(self):
        a = self.artboard('iphone', '--scheme', 'dark')
        roda('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual([c['w'] for c in self.chamadas], [736, 415 + 24])

    def test_shot_com_theme_so_tira_esse_esquema(self):
        a = self.artboard('browser', '--scheme', 'both', '--widths', '1280')
        roda('shot', a, '--out-dir', os.path.join(self.dir, 'png'), '--theme', 'dark')
        self.assertEqual([c['theme'] for c in self.chamadas], ['dark'] * 2)

    def test_shot_erro_do_png_sai_1(self):
        artboard.gera_png = lambda *a, **k: 'brza shot falhou'
        a = self.artboard('macos')
        rc, _, err = roda('shot', a, '--out-dir', os.path.join(self.dir, 'png'))
        self.assertEqual(rc, 1)
        self.assertIn('brza shot falhou', err)

    def test_shot_de_arquivo_que_nao_e_artboard(self):
        x = os.path.join(self.dir, 'x.html')
        self.escreve(x, '<p>oi</p>')
        self.assertEqual(roda('shot', x, '--out-dir', self.dir)[0], 1)

    def test_promote_plano(self):
        raiz = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(raiz, 'plans', 'PLN-099-um-plano'))
        a = self.artboard('macos')
        rc, out, err = roda('promote', a, '--plan', 'PLN-099', '--name', 'Lista de Chats', '--root', raiz)
        self.assertEqual(rc, 0, err)
        png = os.path.join(raiz, 'plans', 'PLN-099-um-plano', 'PLN-099-lista-de-chats.png')
        self.assertTrue(os.path.isfile(png))
        self.assertIn('![lista de chats](PLN-099-lista-de-chats.png)', out)
        self.assertEqual(self.chamadas[0]['w'], 1304)
        self.assertEqual(self.chamadas[0]['scale'], 2)

    def test_promote_escolhe_largura_e_esquema(self):
        raiz = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(raiz, 'plans', 'PLN-099-x'))
        _, out, _, _ = self.novo('w', 'browser', '--pack', 'brza-studio')
        a = re.search(r'^arquivo: (.*)$', out, re.M).group(1)
        rc, _, _ = roda('promote', a, '--plan', '99', '--name', 'tablet', '--width', '768', '--scheme', 'dark',
                        '--root', raiz)
        self.assertEqual(rc, 0)
        self.assertEqual((self.chamadas[0]['w'], self.chamadas[0]['theme']), (768 + 24, 'dark'))
        self.assertEqual(roda('promote', a, '--plan', '99', '--name', 'x', '--width', '999', '--root', raiz)[0], 2)

    def test_promote_issue_grava_ao_lado(self):
        raiz = os.path.join(self.dir, 'repo')
        os.makedirs(os.path.join(raiz, 'work', 'issues'))
        self.escreve(os.path.join(raiz, 'work', 'issues', 'ISS-001-tela.md'), '# x\n')
        a = self.artboard('macos')
        rc, out, err = roda('promote', a, '--issue', 'work/issues/ISS-001-tela.md', '--name', 'v1', '--root', raiz)
        self.assertEqual(rc, 0, err)
        self.assertTrue(os.path.isfile(os.path.join(raiz, 'work', 'issues', 'ISS-001-tela-v1.png')))

    def test_promote_sem_a_pasta_do_plano_sai_1(self):
        a = self.artboard('macos')
        rc, _, err = roda('promote', a, '--plan', 'PLN-077', '--name', 'x', '--root', self.dir)
        self.assertEqual(rc, 1)
        self.assertIn('PLN-077', err)


class Saida(unittest.TestCase):
    def test_pasta_de_saida(self):
        self.assertEqual(artboard.pasta_saida('/x'), ('/x', True))
        os.environ.pop('ORCA_CHAT_SCRATCH_DIR', None)
        self.assertFalse(artboard.pasta_saida(None)[1])


if __name__ == '__main__':
    unittest.main()
