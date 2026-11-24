"""Изменения затрагивают только дерево текущего сеанса."""

import copy
import posixpath


def rmdir(shell, path):
    target = shell.absolute(path)
    item = shell.node(target)
    if not isinstance(item, dict) or item:
        raise ValueError("rmdir ожидает пустой каталог")
    if target in ("/", shell.cwd):
        raise ValueError("Каталог занят")
    del shell.node(posixpath.dirname(target))[posixpath.basename(target)]


def duplicate(shell, args):
    recursive = args[:1] == ["-r"]
    paths = args[1:] if recursive else args
    if len(paths) != 2:
        raise ValueError("Использование: cp [-r] источник назначение")
    source, dest = map(shell.absolute, paths)
    item = shell.node(source)
    if source == "/" or isinstance(item, dict) and not recursive:
        raise ValueError("Для подкаталога используйте cp -r")
    parent = shell.node(posixpath.dirname(dest))
    name = posixpath.basename(dest)
    if not isinstance(parent, dict):
        raise ValueError("Назначение не является каталогом")
    if dest == "/" or isinstance(parent.get(name), dict):
        parent = shell.node(dest)
        name = posixpath.basename(source)
        dest = posixpath.join(dest, name)
    if dest == source or dest.startswith(source + "/"):
        raise ValueError("Нельзя копировать в себя")
    if name in parent and (isinstance(item, dict) or isinstance(parent[name], dict)):
        raise ValueError("Назначение занято каталогом или конфликтует по типу")
    parent[name] = copy.deepcopy(item)

