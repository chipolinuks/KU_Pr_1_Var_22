"""Модуль виртуальной файловой системы"""

import json
import base64
from pathlib import Path


class VirtualFileSystem:
    """Виртуальная файловая система на основе JSON"""

    def __init__(self):
        """Инициализировать пустую VFS"""
        self.root = {
            "type": "directory",
            "name": "/",
            "children": {}
        }
        self.current_path = "/"

    def resolve_path(self, path):
        """Разрешить относительный или абсолютный путь"""
        if path.startswith("/"):
            parts = path.strip("/").split("/")
        else:
            current_parts = self.current_path.strip("/").split("/")
            if self.current_path == "/":
                current_parts = []
            parts = current_parts + path.strip("/").split("/")

        resolved = []
        for part in parts:
            if part == "..":
                if resolved:
                    resolved.pop()
            elif part and part != ".":
                resolved.append(part)

        return "/" + "/".join(resolved) if resolved else "/"

    def load_from_json(self, file_path):
        """Загрузить VFS из JSON-файла"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл VFS не найден: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Неверный формат JSON: {e}")

        self.root = data
        if "name" not in self.root or "type" not in self.root:
            raise ValueError("Неверная структура VFS")

    def get_node(self, path):
        """Получить узел по пути"""
        if path == "/":
            return self.root

        parts = path.strip("/").split("/")
        current = self.root

        for part in parts:
            if current["type"] != "directory":
                return None
            if part not in current["children"]:
                return None
            current = current["children"][part]

        return current

    def list_directory(self, path):
        """Список содержимого директории"""
        node = self.get_node(path)
        if node is None or node["type"] != "directory":
            return None
        return list(node["children"].keys())

    def get_file_content(self, path):
        """Получить содержимое файла по пути"""
        node = self.get_node(path)
        if node is None or node["type"] != "file":
            return None, f"файл не найден: {path}"

        content = node.get("content", "")
        if node.get("encoding") == "base64":
            try:
                content = base64.b64decode(content).decode("utf-8", errors="replace")
            except Exception:
                content = "[binary data]"

        return content, None