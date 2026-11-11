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
CSS_DRIFT = os.path.join(FIX, 'mini-deriva.css')
TS = os.path.join(FIX, 'mini-theme.ts')


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = tokens.main(list(argv))
    return rc, out.getvalue(), err.getvalue()


class Extract(unittest.TestCase):
    def setUp(self):
        self.pack = tokens.build_brza(CSS, TS)
        self.l, self.d = self.pack['schemes']['light'], self.pack['schemes']['dark']

    def test_root_and_dark_with_cascade(self):
        self.assertEqual(self.l['background'], '#fff')
        self.assertEqual(self.d['background'], '#0a0a0a')
        self.assertEqual(self.d['border'], 'rgb(255 255 255 / 0.07)')
        self.assertEqual(self.d['radius'], '0.625rem')            # só no :root: o escuro herda
        self.assertNotIn('so-light', self.l)  # fora da lista, não entra

    def test_the_media_block_does_not_count(self):
        self.assertEqual(self.l['background'], '#fff')

    def test_blocks_grouped_by_comma(self):
        self.assertEqual(self.l['destructive'], '#e40014')
        self.assertEqual(self.d['destructive'], '#ff6568')

    def test_var_of_tailwind_and_source_resolved(self):
        self.assertEqual(self.l['chart-1'], '#93c5fd')
        self.assertEqual(self.pack['fonts']['sans'], "'Geist', sans-serif")
        self.assertNotIn('font-sans', self.l)

    def test_mobile_by_scope_with_comments(self):
        self.assertEqual(self.l['m-bg-base'], '#ffffff')
        self.assertEqual(self.d['m-border-subtle'], 'rgba(255, 255, 255, 0.07)')
        self.assertEqual(self.pack['spaces']['m-space-sm'], '8px')
        self.assertEqual(self.pack['spaces']['m-radius-control'], '12px')
        self.assertEqual(self.pack['spaces']['m-text-title'], '18px')
        self.assertNotIn('m-text-mono-family', self.pack['spaces'])

    def test_origin_with_sha256(self):
        self.assertEqual(len(self.pack['origin']['desktop']['sha256']), 64)
        self.assertEqual(self.pack['origin']['mobile']['file'], TS)

    def test_generic_takes_everything_of_css(self):
        p = tokens.build_generic('x', CSS)
        self.assertEqual(p['schemes']['light']['so-light'], '#123456')
        self.assertEqual(p['origin']['desktop']['file'], CSS)


class CheckPack(unittest.TestCase):
    def extracts(self, tmp):
        rc, _, _ = run('extract', 'brza-studio', '--src', CSS, '--mobile-src', TS, '--packs-dir', tmp)
        self.assertEqual(rc, 0)

    def test_up_to_date_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extracts(tmp)
            rc, out, _ = run('check', 'brza-studio', '--src', CSS, '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 0)
            self.assertIn('em dia', out)

    def test_drift_exits_4_and_lists_the_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extracts(tmp)
            rc, _, err = run('check', 'brza-studio', '--src', CSS_DRIFT, '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 4)
            self.assertIn('deriva', err)
            self.assertIn('2 tokens: --primary, --sidebar', err)
            self.assertIn('rode tokens.py extract brza-studio', err)

    def test_source_changed_without_token_changed_is_not_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extracts(tmp)
            other = os.path.join(tmp, 'outro.css')
            with open(CSS, encoding='utf-8') as f, open(other, 'w', encoding='utf-8') as g:
                g.write(f.read() + '\n.x { color: red; }\n')
            rc, out, _ = run('check', 'brza-studio', '--src', other, '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 0)
            self.assertIn('nenhum token', out)

    def test_source_missing_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.extracts(tmp)
            rc, _, err = run('check', 'brza-studio', '--src', os.path.join(tmp, 'nao-existe.css'),
                              '--mobile-src', TS, '--packs-dir', tmp)
            self.assertEqual(rc, 1)
            self.assertIn('fonte ausente', err)

    def test_extract_with_source_missing_exits_1_and_project_without_src_also(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run('extract', 'brza-studio', '--src', '/nope.css', '--mobile-src', TS,
                                  '--packs-dir', tmp)[0], 1)
            self.assertEqual(run('extract', 'outro', '--packs-dir', tmp)[0], 1)

    def test_pack_missing_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run('check', 'brza-studio', '--packs-dir', tmp)[0], 1)

    def test_neutral_has_nothing_to_check(self):
        self.assertEqual(run('check', 'neutral')[0], 0)

    def test_list_prints_the_names_sa(self):
        rc, out, _ = run('list')
        self.assertEqual(rc, 0)
        self.assertIn('--sa-background', out)
        self.assertIn('neutral', out)


class RealPacks(unittest.TestCase):
    def test_the_26_names_in_two_packs(self):
        for name in ('brza-studio', 'neutral'):
            p = tokens.load(name)
            name_list = set(tokens.pack_names(p))
            still_missing = [n for n in tokens.ORCA_NAMES if '--sa-' + n not in name_list]
            self.assertEqual(still_missing, [], name)
            for e in ('light', 'dark'):
                self.assertTrue(p['schemes'][e]['background'])

    def test_brza_studio_has_the_mobile(self):
        p = tokens.load('brza-studio')
        self.assertIn('m-bg-panel', p['schemes']['dark'])
        self.assertIn('m-radius-surface', p['spaces'])


if __name__ == '__main__':
    unittest.main()
