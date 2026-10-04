"""Модуль оболочки эмулятора"""

import shlex
from src.vfs import VirtualFileSystem


class Shell:
    """Класс оболочки эмулятора командной строки"""

    def __init__(self, vfs_path=None):
        """Инициализировать оболочку"""
        self.running = True
        self.vfs = VirtualFileSystem()
        self.vfs_path = vfs_path
        self.vfs_load_message = "VFS не загружена: путь не указан"

        if vfs_path:
            try:
                self.vfs.load_from_json(vfs_path)
                self.vfs_load_message = f"VFS успешно загружена из {vfs_path}"
            except FileNotFoundError as e:
                self.vfs_load_message = f"Ошибка загрузки VFS: {e}"
            except ValueError as e:
                self.vfs_load_message = f"Ошибка загрузки VFS: {e}"

        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }

    def parse_command(self, line):
        """Разобрать строку ввода на команду и аргументы"""
        line = line.strip()
        if not line:
            return None, None, None
        try:
            parts = shlex.split(line)
        except ValueError:
            return None, None, "Ошибка: некорректные кавычки в аргументах"
        if not parts:
            return None, None, None
        return parts[0], parts[1:], None

    def execute(self, command, args):
        """Выполнить команду с аргументами"""
        if command in self.commands:
            return self.commands[command](args)
        return f"Ошибка: неизвестная команда '{command}'"

    def cmd_ls(self, args):
        """Команда ls — список содержимого директории"""
        path = args[0] if args else self.vfs.current_path
        items = self.vfs.list_directory(path)
        if items is None:
            return f"Ошибка: путь '{path}' не найден или не является директорией"
        if not items:
            return f"Директория '{path}' пуста"
        return "\n".join(items)

    def cmd_cd(self, args):
        """Команда cd — смена текущей директории"""
        if not args:
            self.vfs.current_path = "/"
            return "Переход в корневую директорию"

        target = args[0]
        if target.startswith("/"):
            new_path = target
        else:
            if self.vfs.current_path == "/":
                new_path = f"/{target}"
            else:
                new_path = f"{self.vfs.current_path}/{target}"

        node = self.vfs.get_node(new_path)
        if node is None:
            return f"Ошибка: директория '{target}' не найдена"
        if node["type"] != "directory":
            return f"Ошибка: '{target}' не является директорией"

        self.vfs.current_path = new_path
        return f"Переход в '{new_path}'"

    def cmd_exit(self, args):
        """Команда выхода из оболочки"""
        self.running = False
        return "Выход из эмулятора"

    def is_running(self):
        """Проверить, работает ли оболочка"""
        return self.running

    def run_script(self, file_path):
        """Выполнить команды из стартового скрипта"""
        results = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    command, args, error = self.parse_command(line)
                    if error is not None:
                        results.append((line, error))
                        continue
                    if command is None:
                        continue
                    result = self.execute(command, args)
                    results.append((line, result))
        except FileNotFoundError:
            results.append(("", f"Ошибка: файл скрипта '{file_path}' не найден"))
        except Exception as e:
            results.append(("", f"Ошибка чтения скрипта: {e}"))
        return results