from test_shell import ROOT, Shell
import unittest

from main import Terminal, start_script
from types import SimpleNamespace

IMAGE = ROOT / "examples/deep.json"


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.shell = Shell(IMAGE)

    def test_text(self):
        run = self.shell.execute
        run('cd "мои файлы/неделя/лаб"')
        self.assertEqual(run("cat стих.txt"), "мир\nRuby\n")
        self.assertEqual(run("rev стих.txt"), "рим\nybuR\n")
        self.assertEqual(run("tac стих.txt"), "Ruby\nмир\n")

    def test_changes_in_memory(self):
        original = IMAGE.read_bytes()
        run = self.shell.execute
        run("rmdir пусто")
        run('cp -r "мои файлы" архив')
        run('cp архив/неделя/лаб/стих.txt архив/новый')
        self.assertNotIn("новый", run('ls "мои файлы"'))
        with self.assertRaises(ValueError):
            run("rmdir архив")
        self.assertEqual(IMAGE.read_bytes(), original)
        self.assertIn("пусто", Shell(IMAGE).execute("ls"))

    def test_script_continues(self):
        output = []
        terminal = Terminal.__new__(Terminal)
        terminal.shell = self.shell
        terminal.root = SimpleNamespace(
            after=lambda delay, fn, index: fn(index), destroy=lambda: None)
        terminal.write = output.append
        start_script(terminal, ROOT / "examples/errors.txt")
        self.assertTrue(self.shell.closed)
        self.assertIn("пусто", "\n".join(output))
        self.assertEqual(sum(s.startswith("Ошибка") for s in output), 2)

