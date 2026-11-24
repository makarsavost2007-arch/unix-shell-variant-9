import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shell import Shell


class ShellTests(unittest.TestCase):
    def test_exit(self):
        shell = Shell()
        shell.execute("exit")
        self.assertTrue(shell.closed)

    def test_errors(self):
        for command in ("unknown", "exit 2", 'cd "missing'):
            with self.subTest(command=command), self.assertRaises(ValueError):
                Shell().execute(command)

