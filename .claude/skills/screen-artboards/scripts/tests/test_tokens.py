"""Testes do tokens.py: a extração do CSS e do TS, a deriva e os códigos de saída."""
import contextlib
import io
import json
import os
import tempfile
import unittest

import _paths  # noqa: F401
import tokens

FIX = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
CSS = os.path.join(FIX, 'mini.css')
CSS_DERIVA = os.path.join(FIX, 'mini-deriva.css')
TS = os.path.join(FIX, 'mini-theme.ts')


def roda(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = tokens.main(list(argv))
    return rc, out.getvalue(), err.getvalue()


class Extrai(unittest.TestCase):
    def setUp(self):
        self.pack = tokens.monta_brza(CSS, TS)
        self.l, self.d = self.pack['esquemas']['light'], self.pack['esquemas']['dark']

    def test_root_e_dark_com_cascata(self):
        self.assertEqual(self.l['background'], '#fff')
        self.assertEqual(self.d['background'], '#0a0a0a')
        self.assertEqual(self.d['border'], 'rgb(255 255 255 / 0.07)')
        self.assertEqual(self.d['radius'], '0.625rem')            # só no :root: o escuro herda
        self.assertNotIn('so-light', self.l)  # fora da lista, não entra

    def test_o_bloco_de_media_nao_vale(self):
        self.assertEqual(self.l['background'], '#fff')

    def test_blocos_agrupados_por_virgula(self):
        self.assertEqual(self.l['destructive'], '#e40014')
        self.assertEqual(self.d['destructive'], '#ff6568')

    def test_var_do_tailwind_e_fonte_resolvidas(self):
        self.assertEqual(self.l['chart-1'], '#93c5fd')
        self.assertEqual(self.pack['fontes']['sans'], "'Geist', sans-serif")
        self.assertNotIn('font-sans', self.l)

    def test_mobile_por_escopo_com_comentarios(self):
        self.assertEqual(self.l['m-bg-base'], '#ffffff')
        self.assertEqual(self.d['m-border-subtle'], 'rgba(255, 255, 255, 0.07)')
        self.assertEqual(self.pack['espacos']['m-space-sm'], '8px')
        self.assertEqual(self.pack['espacos']['m-radius-control'], '12px')
        self.assertEqual(self.pack['espacos']['m-text-title'], '18px')
        self.assertNotIn('m-text-mono-family', self.pack['espacos'])

    def test_origem_com_sha256(self):
        self.assertEqual(len(self.pack['origem']['desktop']['sha256']), 64)
        self.assertEqual(self.pack['origem']['mobile']['arquivo'], TS)

    def test_generico_leva_tudo_do_css(self):
        p = tokens.monta_generico('x', CSS)
        self.assertEqual(p['esquemas']['light']['so-light'], '#123456')
        self.assertEqual(p['origem']['desktop']['arquivo'], CSS)


class Confere(unittest.TestCase):
    def extrai(self, tmp):
        rc, _, _ = roda('extract', 'brza-studio', '--src', CSS, '--mobile-src', TS, '--packs-dir', tmp)
        self.assertEqual(rc, 0)

    def test_em_dia_sai_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extrai(tmp)
            rc, out, _ = roda('check', 'brza-studio', '--src', CSS, '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 0)
            self.assertIn('em dia', out)

    def test_deriva_sai_4_e_lista_os_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extrai(tmp)
            rc, _, err = roda('check', 'brza-studio', '--src', CSS_DERIVA, '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 4)
            self.assertIn('deriva', err)
            self.assertIn('2 tokens: --primary, --sidebar', err)
            self.assertIn('rode tokens.py extract brza-studio', err)

    def test_fonte_mudada_sem_token_mudado_nao_e_deriva(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extrai(tmp)
            outro = os.path.join(tmp, 'outro.css')
            with open(CSS, encoding='utf-8') as f, open(outro, 'w', encoding='utf-8') as g:
                g.write(f.read() + '\n.x { color: red; }\n')
            rc, out, _ = roda('check', 'brza-studio', '--src', outro, '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 0)
            self.assertIn('nenhum token', out)

    def test_fonte_ausente_sai_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extrai(tmp)
            rc, _, err = roda('check', 'brza-studio', '--src', os.path.join(tmp, 'nao-existe.css'),
                              '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 1)
            self.assertIn('fonte ausente', err)

    def test_extract_com_fonte_ausente_sai_1_e_projeto_sem_src_tambem(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(roda('extract', 'brza-studio', '--src', '/nope.css', '--mobile-src', TS,
                                  '--packs-dir', tmp)[0], 1)
            self.assertEqual(roda('extract', 'outro', '--packs-dir', tmp)[0], 1)

    def test_pacote_ausente_sai_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(roda('check', 'brza-studio', '--packs-dir', tmp)[0], 1)

    def test_neutro_nao_tem_o_que_conferir(self):
        self.assertEqual(roda('check', 'neutral')[0], 0)

    def test_list_imprime_os_nomes_sa(self):
        rc, out, _ = roda('list')
        self.assertEqual(rc, 0)
        self.assertIn('--sa-background', out)
        self.assertIn('neutral', out)


class PacotesReais(unittest.TestCase):
    def test_os_26_nomes_nos_dois_pacotes(self):
        for nome in ('brza-studio', 'neutral'):
            p = tokens.carrega(nome)
            nomes = set(tokens.nomes_do_pacote(p))
            faltam = [n for n in tokens.NOMES_ORCA if '--sa-' + n not in nomes]
            self.assertEqual(faltam, [], nome)
            for e in ('light', 'dark'):
                self.assertTrue(p['esquemas'][e]['background'])

    def test_brza_studio_tem_os_do_mobile(self):
        p = tokens.carrega('brza-studio')
        self.assertIn('m-bg-panel', p['esquemas']['dark'])
        self.assertIn('m-radius-surface', p['espacos'])


if __name__ == '__main__':
    unittest.main()
