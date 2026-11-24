"""Операции над виртуальным деревом; файлы хранятся как bytes."""

import posixpath
import shlex

from vfs import load


class Shell:
    def __init__(self, path=None):
        self.name, self.root = load(path)
        self.cwd = "/"
        self.closed = False

    def node(self, path):
        item = self.root
        for part in filter(None, path.split("/")):
            if not isinstance(item, dict) or part not in item:
                raise ValueError(f"Путь не найден: {path}")
            item = item[part]
        return item

    def absolute(self, path):
        if not path:
            raise ValueError("Пустой путь")
        current = "/" if path.startswith("/") else self.cwd
        for part in path.split("/"):
            if not part:
                continue
            if not isinstance(self.node(current), dict):
                raise ValueError(f"Это не каталог: {current}")
            if part == "..":
                current = posixpath.dirname(current)
            elif part != ".":
                current = posixpath.join(current, part)
        if path.endswith("/") and not isinstance(self.node(current), dict):
            raise ValueError(f"Это не каталог: {current}")
        return current

    def listing(self, path):
        item = self.node(path)
        if isinstance(item, dict):
            return "\n".join(sorted(item))
        return posixpath.basename(path)

    def text(self, name, path):
        data = self.node(self.absolute(path))
        if isinstance(data, dict):
            raise ValueError(f"Ожидался файл: {path}")
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"Файл не является текстом UTF-8: {path}") from error
        if name == "cat":
            return content
        lines = content.splitlines(keepends=True)
        if name == "tac":
            return "".join(reversed(lines))
        result = []
        for line in lines:
            body = line.rstrip("\r\n")
            result.append(body[::-1] + line[len(body):])
        return "".join(result)

    def execute(self, line):
        words = shlex.split(line)
        if not words:
            return ""
        name, *args = words
        if name == "exit" and not args:
            self.closed = True
            return ""
        if name in ("ls", "cd") and len(args) <= 1:
            path = self.absolute(args[0] if args else ("/" if name == "cd" else "."))
            if name == "ls":
                return self.listing(path)
            if not isinstance(self.node(path), dict):
                raise ValueError(f"Это не каталог: {path}")
            self.cwd = path
            return ""
        if name in ("cat", "tac", "rev") and args:
            return "".join(self.text(name, path) for path in args)
        if name in ("ls", "cd", "cat", "tac", "rev", "exit"):
            raise ValueError(f"{name}: неверные аргументы")
        raise ValueError(f"Неизвестная команда: {name}")

