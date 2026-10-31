"""Testes do brza-tree, num brza-studio de mentira: um clone de uma origin local, com o install trocado por um falso.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import io
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS))
import brza_runtime as runtime  # noqa: E402

TREE = runpy.run_path(str(SCRIPTS / 'brza-tree'))
# As funções leem os globais do módulo em que nasceram, não da cópia que o run_path devolve.
GLOBALS = TREE['main'].__globals__


def git(*args, cwd: Path):
    return subprocess.run(['git', '-C', str(cwd), '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


class TreeBase(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        origin, self.seed, self.studio = self.base / 'origin.git', self.base / 'seed', self.base / 'studio'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'master', str(origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(origin), str(self.seed)], check=True, capture_output=True)
        git('commit', '-q', '--allow-empty', '-m', 'um', cwd=self.seed)
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.seed)
        subprocess.run(['git', 'clone', '-q', str(origin), str(self.studio)], check=True)
        # um commit que só chega ao studio pelo fetch
        git('commit', '-q', '--allow-empty', '-m', 'dois', cwd=self.seed)
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.seed)
        self.tip = git('rev-parse', 'HEAD', cwd=self.seed)
        self.installed = []
        self.install_error = None
        for p in (patch.object(runtime, 'STUDIO', self.studio),
                  patch.object(runtime, 'install_offline', self.fake_install)):
            p.start()
            self.addCleanup(p.stop)

    def fake_install(self, path: Path):
        self.installed.append(path)
        if self.install_error:
            raise runtime.BrzaError(self.install_error)

    def run_tree(self, *argv) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                code = GLOBALS['main'](list(argv))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue()

    def tree(self, name: str) -> Path:
        return self.studio / '.worktrees' / name

    def branches(self) -> list[str]:
        return git('branch', '--format=%(refname:short)', cwd=self.studio).splitlines()

    def commit_in(self, path: Path, message: str = 'trabalho'):
        git('commit', '-q', '--allow-empty', '-m', message, cwd=path)


class TreeTest(TreeBase):
    # criar

    def test_creates_feat_branch_from_fetched_origin_master_and_installs(self):
        code, out = self.run_tree('x')
        self.assertEqual(code, 0, out)
        path = self.tree('x')
        self.assertEqual(git('rev-parse', '--abbrev-ref', 'HEAD', cwd=path), 'feat/x')
        self.assertEqual(git('rev-parse', 'HEAD', cwd=path), self.tip)
        self.assertEqual(self.installed, [path])
        self.assertIn(str(path), out)

    def test_type_and_base_choose_the_branch_and_the_start(self):
        first = git('rev-parse', 'HEAD~1', cwd=self.seed)
        code, out = self.run_tree('y', '--type', 'fix', '--base', first)
        self.assertEqual(code, 0, out)
        self.assertEqual(git('rev-parse', '--abbrev-ref', 'HEAD', cwd=self.tree('y')), 'fix/y')
        self.assertEqual(git('rev-parse', 'HEAD', cwd=self.tree('y')), first)

    def test_failed_offline_install_keeps_the_worktree_and_prints_the_command(self):
        self.install_error = 'o install offline falhou'
        code, out = self.run_tree('x')
        self.assertEqual(code, 1)
        self.assertTrue(self.tree('x').is_dir())
        self.assertIn(str(self.tree('x')), out)
        self.assertIn('pnpm install --frozen-lockfile', out)

    def test_existing_directory_is_refused(self):
        self.tree('x').mkdir(parents=True)
        code, out = self.run_tree('x')
        self.assertEqual(code, 1)
        self.assertIn('já existe', out)
        self.assertEqual(self.installed, [])

    def test_chat_opens_the_session_in_the_worktree(self):
        calls = self.base / 'calls'
        fake = self.base / 'brza-sessions'
        fake.write_text(f'#!/bin/sh\necho "$*" > {calls}\n')
        fake.chmod(0o755)
        with patch.dict(GLOBALS, {'SESSIONS': fake}):
            code, out = self.run_tree('x', '--chat', 'pln-009-p1')
        self.assertEqual(code, 0, out)
        self.assertEqual(calls.read_text().strip(), f'pln-009-p1 --checkout {self.tree("x")}')

    def test_usage_errors_exit_2(self):
        for argv in ([], ['x', '--list'], ['--rm', 'x', '--list'], ['a/b'], ['x', '--force'], ['x', '--empty'],
                     ['--rm', 'x', '--chat', 's'], ['x', '--type', 'wip']):
            with self.subTest(argv=argv):
                self.assertEqual(self.run_tree(*argv)[0], 2)

    # remover

    def test_rm_takes_the_merged_clean_worktree_and_its_branch(self):
        self.run_tree('x')
        self.commit_in(self.tree('x'))
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.tree('x'))
        code, out = self.run_tree('--rm', 'x')
        self.assertEqual(code, 0, out)
        self.assertFalse(self.tree('x').exists())
        self.assertNotIn('feat/x', self.branches())

    def test_rm_refuses_the_dirty_worktree_without_force(self):
        self.run_tree('x')
        self.commit_in(self.tree('x'))
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.tree('x'))
        (self.tree('x') / 'novo.txt').write_text('x')
        code, out = self.run_tree('--rm', 'x')
        self.assertEqual(code, 1)
        self.assertIn('sujo', out)
        self.assertTrue(self.tree('x').exists())
        code, out = self.run_tree('--rm', 'x', '--force')
        self.assertEqual(code, 0, out)
        self.assertIn('descartado: o worktree está sujo', out)
        self.assertFalse(self.tree('x').exists())
        self.assertNotIn('feat/x', self.branches())

    def test_rm_refuses_the_unmerged_branch_without_force(self):
        self.run_tree('x')
        self.commit_in(self.tree('x'))
        code, out = self.run_tree('--rm', 'x')
        self.assertEqual(code, 1)
        self.assertIn('origin/master', out)
        self.assertIn('feat/x', self.branches())
        code, out = self.run_tree('--rm', 'x', '--force')
        self.assertEqual(code, 0, out)
        self.assertIn('descartado: o HEAD não está na origin/master', out)
        self.assertNotIn('feat/x', self.branches())

    def test_rm_asks_empty_for_the_branch_without_own_commit_and_force_does_not_cover_it(self):
        self.run_tree('x')
        code, out = self.run_tree('--rm', 'x')
        self.assertEqual(code, 1)
        self.assertIn('sem commit próprio', out)
        self.assertIn('--empty', out)
        code, out = self.run_tree('--rm', 'x', '--force')
        self.assertEqual(code, 1, out)
        self.assertTrue(self.tree('x').exists())
        code, out = self.run_tree('--rm', 'x', '--empty')
        self.assertEqual(code, 0, out)
        self.assertFalse(self.tree('x').exists())
        self.assertNotIn('feat/x', self.branches())

    def test_empty_does_not_cover_the_dirty_worktree(self):
        self.run_tree('x')
        (self.tree('x') / 'novo.txt').write_text('trabalho do dia')
        code, out = self.run_tree('--rm', 'x', '--empty')
        self.assertEqual(code, 1, out)
        self.assertIn('sujo', out)
        self.assertTrue((self.tree('x') / 'novo.txt').exists())
        code, out = self.run_tree('--rm', 'x', '--empty', '--force')
        self.assertEqual(code, 0, out)
        self.assertFalse(self.tree('x').exists())

    def test_rm_takes_the_detached_worktree_on_origin_master(self):
        runtime.worktree_add(self.tree('conferencia'))
        code, out = self.run_tree('--rm', 'conferencia')
        self.assertEqual(code, 0, out)
        self.assertFalse(self.tree('conferencia').exists())

    def test_rm_lists_the_orphan_and_removes_it_only_with_force(self):
        orphan = self.tree('orfao')
        (orphan / '.cache').mkdir(parents=True)
        (orphan / '.cache' / 'x').write_text('x')
        code, out = self.run_tree('--rm', 'orfao')
        self.assertEqual(code, 1)
        self.assertIn('.cache', out)
        self.assertTrue(orphan.exists())
        code, out = self.run_tree('--rm', 'orfao', '--force')
        self.assertEqual(code, 0, out)
        self.assertIn('.cache', out)
        self.assertFalse(orphan.exists())

    def test_rm_of_nothing_is_refused(self):
        self.assertEqual(self.run_tree('--rm', 'nada')[0], 1)

    # listar

    def test_list_shows_branch_ahead_state_and_orphans(self):
        self.run_tree('x')
        self.commit_in(self.tree('x'))
        (self.tree('x') / 'novo.txt').write_text('x')
        runtime.worktree_add(self.tree('conferencia'))
        (self.tree('orfao') / '.cache').mkdir(parents=True)
        code, out = self.run_tree('--list')
        self.assertEqual(code, 0, out)
        lines = {line.split()[0]: line for line in out.splitlines() if line.strip()}
        self.assertRegex(lines['x'], r'feat/x\s+1 à frente\s+sujo')
        self.assertRegex(lines['conferencia'], r'detached\s+0 à frente\s+limpo')
        self.assertIn('órfão', lines['orfao'])
        self.assertNotIn('studio', lines)


class MemoryTest(TreeBase):
    """A memória da sessão do worktree com pln-NNN: a do workstream do plano, num brza-workspace de mentira com um
    bare como origin e o workstream studio, que tem o PLN-001, num worktree."""

    def setUp(self):
        super().setUp()
        self.ws_origin, self.ws = self.base / 'ws-origin.git', self.base / 'ws'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'master', str(self.ws_origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(self.ws_origin), str(self.ws)], check=True, capture_output=True)
        git('commit', '-q', '--allow-empty', '-m', 'norma', cwd=self.ws)
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.ws)
        self.stream = self.ws / '.worktrees' / 'studio'
        git('worktree', 'add', '-q', '-b', 'workstream/studio', str(self.stream), cwd=self.ws)
        plan = self.stream / 'plans' / 'PLN-001-x' / 'PLN-001-plan.md'
        plan.parent.mkdir(parents=True)
        plan.write_text('# plano\n')
        git('add', '.', cwd=self.stream)
        git('commit', '-q', '-m', 'docs: PLN-001', cwd=self.stream)
        git('push', '-q', '-u', 'origin', 'workstream/studio', cwd=self.stream)
        patcher = patch.object(runtime, 'WORKSPACE', self.ws)
        patcher.start()
        self.addCleanup(patcher.stop)

    def memory_of(self, name: str) -> str | None:
        path = self.tree(name) / '.claude' / 'settings.local.json'
        return json.loads(path.read_text())['autoMemoryDirectory'] if path.exists() else None

    def test_the_plan_worktree_points_the_memory_at_the_workstream_of_the_plan(self):
        code, out = self.run_tree('pln-001-p1')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.memory_of('pln-001-p1'), str(self.stream / 'memory'))
        self.assertIn(f'memória:  {self.stream / "memory"}', out)
        self.assertEqual(self.installed, [self.tree('pln-001-p1')])

    def test_the_memory_is_linked_even_when_the_install_fails(self):
        self.install_error = 'o install offline falhou'
        code, out = self.run_tree('pln-001-p2')
        self.assertEqual(code, 1, out)
        self.assertEqual(self.memory_of('pln-001-p2'), str(self.stream / 'memory'))

    def test_the_type_does_not_matter_only_pln_in_the_branch(self):
        code, out = self.run_tree('pln-001-docs', '--type', 'docs')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.memory_of('pln-001-docs'), str(self.stream / 'memory'))

    def test_a_plan_in_no_workstream_warns_and_goes_on_without_the_memory(self):
        code, out = self.run_tree('pln-009-p1')
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r'aviso: .*PLN-009 não está em nenhum workstream')
        self.assertIsNone(self.memory_of('pln-009-p1'))
        self.assertEqual(self.installed, [self.tree('pln-009-p1')])

    def test_a_workstream_without_a_worktree_warns_with_the_command_that_creates_it(self):
        git('worktree', 'remove', '--force', str(self.stream), cwd=self.ws)
        code, out = self.run_tree('pln-001-p3')
        self.assertEqual(code, 0, out)
        self.assertIn('aviso:', out)
        self.assertIn('brza note workstream studio', out)
        self.assertIsNone(self.memory_of('pln-001-p3'))

    def test_a_branch_without_pln_has_no_lookup_and_no_warning(self):
        code, out = self.run_tree('x')
        self.assertEqual(code, 0, out)
        self.assertNotIn('aviso', out)
        self.assertNotIn('memória', out)
        self.assertIsNone(self.memory_of('x'))

    def test_unreadable_local_settings_warn_and_do_not_stop_the_tree(self):
        def broken(path, memory):
            raise runtime.BrzaError('settings.local.json ilegível')

        with patch.object(runtime, 'set_auto_memory', broken):
            code, out = self.run_tree('pln-001-p4')
        self.assertEqual(code, 0, out)
        self.assertIn('aviso:', out)
        self.assertIn('ilegível', out)

    def test_the_agent_memory_is_a_symlink_to_the_workstream_created_when_missing(self):
        target = self.stream / '.claude' / 'agent-memory'
        self.assertFalse(target.exists())
        code, out = self.run_tree('pln-001-p5')
        self.assertEqual(code, 0, out)
        link = self.tree('pln-001-p5') / '.claude' / 'agent-memory'
        self.assertTrue(link.is_symlink())
        self.assertEqual(Path(os.readlink(link)), target)
        self.assertTrue(target.is_dir())
        self.assertIn(f'agentes:  {link} -> {target}', out)
        (target / 'reviewer').mkdir()
        (link / 'reviewer' / 'achados.md').write_text('x\n')
        self.assertTrue((target / 'reviewer' / 'achados.md').exists())

    def test_the_agent_memory_keeps_what_the_workstream_already_has(self):
        target = self.stream / '.claude' / 'agent-memory' / 'collector'
        target.mkdir(parents=True)
        (target / 'a.md').write_text('antes\n')
        self.run_tree('pln-001-p6')
        link = self.tree('pln-001-p6') / '.claude' / 'agent-memory'
        self.assertEqual((link / 'collector' / 'a.md').read_text(), 'antes\n')

    def test_a_real_directory_where_the_link_goes_is_not_replaced_and_warns(self):
        link_memory = GLOBALS['link_memory']

        def with_real_directory(path, branch):
            (path / '.claude' / 'agent-memory').mkdir(parents=True)
            (path / '.claude' / 'agent-memory' / 'meu.md').write_text('meu\n')
            return link_memory(path, branch)

        with patch.dict(GLOBALS, {'link_memory': with_real_directory}):
            code, out = self.run_tree('pln-001-p7')
        self.assertEqual(code, 0, out)
        link = self.tree('pln-001-p7') / '.claude' / 'agent-memory'
        self.assertFalse(link.is_symlink())
        self.assertEqual((link / 'meu.md').read_text(), 'meu\n')
        self.assertRegex(out, r'aviso: .*agent-memory já existe e não é um link')

    def test_no_agent_link_without_the_workstream(self):
        code, out = self.run_tree('pln-009-p2')
        self.assertEqual(code, 0, out)
        self.assertFalse((self.tree('pln-009-p2') / '.claude' / 'agent-memory').exists())
        code, out = self.run_tree('y')
        self.assertFalse((self.tree('y') / '.claude' / 'agent-memory').exists())
        self.assertFalse((self.stream / '.claude' / 'agent-memory').exists())


if __name__ == '__main__':
    unittest.main()
