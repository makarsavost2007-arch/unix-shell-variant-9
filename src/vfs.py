"""JSON-образ: объект задаёт каталог, строка Base64 задаёт файл."""

import base64
import binascii
import json


def unique(pairs):
    entries = {}
    for name, value in pairs:
        if name in entries:
            raise ValueError(f"Повтор имени: {name}")
        entries[name] = value
    return entries


def decode(node):
    if isinstance(node, str):
        try:
            return base64.b64decode(node, validate=True)
        except (ValueError, binascii.Error) as error:
            raise ValueError("Некорректные данные Base64") from error
    if not isinstance(node, dict):
        raise ValueError("Узел должен быть каталогом или строкой Base64")
    result = {}
    for name, child in node.items():
        if not name or name in (".", "..") or "/" in name:
            raise ValueError(f"Некорректное имя: {name!r}")
        result[name] = decode(child)
    return result


def load(path):
    if path is None:
        return "default", {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=unique)
        if not isinstance(data, dict):
            raise ValueError("Корень должен быть каталогом")
        return path.stem, decode(data)
    except (OSError, ValueError) as error:
        raise ValueError(f"Не удалось загрузить VFS {path}: {error}") from error

