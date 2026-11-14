"""Testes do runtime_memory_check.py, com o HOME apontado para um diretório temporário."""
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import runtime_memory_check as rmc  # noqa: E402

ANTES, INICIO, DEPOIS = "2026-11-07T20:00:00-03:00", "2026-11-07T21:19:00-03:00", "2026-11-07T21:40:00-03:00"


class HoraSemData(unittest.TestCase):
    def test_hh_mm_no_futuro_e_de_ontem(self):
        """M1: reunião que atravessou a meia-noite: `23:58` dito às 00:05 é de ontem, não de daqui a 23 h."""
        agora = datetime.now().astimezone()
        futuro = (agora + timedelta(minutes=30)).strftime("%H:%M")
        d = rmc.parse_start(futuro)
        self.assertLessEqual(d, agora)
        if (agora + timedelta(minutes=30)).date() == agora.date():   # só o relógio deste teste, sem virar o dia
            self.assertEqual(d.date(), agora.date() - timedelta(days=1))
        passado = (agora - timedelta(minutes=30)).strftime("%H:%M")
        if (agora - timedelta(minutes=30)).date() == agora.date():
            self.assertEqual(rmc.parse_start(passado).date(), agora.date())


class Verificacao(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.home, True)
        self._home = os.environ.get("HOME")
        os.environ["HOME"] = self.home
        self.addCleanup(self._restaura)

    def _restaura(self):
        if self._home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = self._home

    def arq(self, rel, quando, conteudo="memória"):
        p = os.path.join(self.home, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(conteudo)
        ts = datetime.fromisoformat(quando).timestamp()
        os.utime(p, (ts, ts))
        return p

    def roda(self, inicio=INICIO, *extra):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = rmc.main([inicio, *extra])
        self.assertEqual(rc, 0)
        return buf.getvalue().strip().split("\n")

    def test_vazio_imprime_nenhum_e_ignora_diretorios_inexistentes(self):
        self.assertEqual(self.roda(), ["nenhum"])

    def test_so_o_que_mudou_depois_do_inicio(self):
        self.arq(".grok/memory-v2/workspaces/w/topics/velho.md", ANTES)
        self.arq(".grok/memory-v2/workspaces/w/topics/reuniao-salto.md", DEPOIS, "12345")
        self.arq(".codex/memories/nota.md", DEPOIS)
        self.arq(".gemini/GEMINI.md", DEPOIS)
        self.arq(".gemini/antigravity/brain/b1/nota.md", DEPOIS)
        self.arq(".gemini/antigravity/log/cli.log", DEPOIS)           # log: fora
        self.arq(".gemini/antigravity/conversations/c.pb", DEPOIS)    # conversa: fora
        self.arq(".claude/projects/-x/memory/feedback.md", DEPOIS)
        self.arq(".claude/projects/-x/outra-coisa.jsonl", DEPOIS)     # fora de memory/
        linhas = self.roda()
        achados = "\n".join(linhas)
        self.assertIn("~/.grok/memory-v2/workspaces/w/topics/reuniao-salto.md · 2026-11-07 21:40:00 · 5 B", achados)
        self.assertNotIn("velho.md", achados)
        self.assertIn("~/.codex/memories/nota.md", achados)
        self.assertIn("~/.gemini/GEMINI.md", achados)
        self.assertIn("~/.gemini/antigravity/brain/b1/nota.md", achados)
        self.assertNotIn("cli.log", achados)
        self.assertNotIn("c.pb", achados)
        self.assertNotIn("outra-coisa", achados)
        claude = [l for l in linhas if "feedback.md" in l]
        self.assertEqual(len(claude), 1)
        self.assertIn("aviso", claude[0])
        self.assertEqual(len(linhas), 5)

    def test_ordem_do_mais_antigo_ao_mais_novo(self):
        self.arq(".grok/memory-v2/b.md", DEPOIS)
        self.arq(".grok/memory-v2/a.md", "2026-11-07T21:30:00-03:00")
        linhas = self.roda()
        self.assertTrue(linhas[0].startswith("~/.grok/memory-v2/a.md"))

    def test_inicio_hh_mm_e_root(self):
        agora = datetime.now().astimezone()
        self.arq(".grok/memory-v2/hoje.md", agora.isoformat())
        inicio = (agora.replace(hour=0, minute=0, second=0, microsecond=0)).strftime("%H:%M")
        self.assertIn("hoje.md", self.roda(inicio)[0])
        # com --root apontando para o diretório da memória, o arquivo conta como dentro do repositório
        self.assertEqual(self.roda(inicio, "--root", os.path.join(self.home, ".grok")), ["nenhum"])

    def test_inicio_iso_sem_fuso(self):
        self.arq(".grok/memory-v2/x.md", DEPOIS)
        self.assertEqual(len(self.roda("2026-11-07T21:19")), 1)


if __name__ == "__main__":
    unittest.main()
