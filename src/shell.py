"""Командный процессор эмулятора."""

import shlex
from vfs import load


class Shell:
    def __init__(self, path=None):
        self.name, self.root = load(path)
        self.cwd = "/"
        self.closed = False

    def execute(self, line):
        words = shlex.split(line)
        if not words:
            return ""
        command, *args = words
        if command in ("ls", "cd") and len(args) <= 1:
            return repr(words)
        if command == "exit" and not args:
            self.closed = True
            return ""
        if command in ("ls", "cd", "exit"):
            raise ValueError(f"{command}: неверные аргументы")
        raise ValueError(f"Неизвестная команда: {command}")
