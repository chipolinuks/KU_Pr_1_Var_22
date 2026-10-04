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
            "head": self.cmd_head,
            "tac": self.cmd_tac,
            "rev": self.cmd_rev,
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
        """Вывести содержимое директории"""
        target = args[0] if args else self.vfs.current_path
        resolved = self.vfs.resolve_path(target)
        node = self.vfs.get_node(resolved)

        if node is None:
            return f"ls: cannot access '{target}': No such file or directory"
        if node["type"] != "directory":
            return f"ls: cannot access '{target}': Not a directory"

        children = node.get("children", {})
        if not children:
            return ""
        return "  ".join(sorted(children.keys()))

    def cmd_cd(self, args):
        """Сменить текущую директорию"""
        if not args:
            self.vfs.current_path = "/"
            return ""

        target = args[0]
        resolved = self.vfs.resolve_path(target)
        node = self.vfs.get_node(resolved)

        if node is None:
            return f"cd: no such file or directory: {target}"
        if node["type"] != "directory":
            return f"cd: not a directory: {target}"

        self.vfs.current_path = resolved
        return ""

    def cmd_head(self, args):
        """Вывести первые 10 строк файла"""
        if not args:
            return "head: missing file operand"

        content, error = self.vfs.get_file_content(self.vfs.resolve_path(args[0]))
        if error:
            return f"head: {error}"

        lines = content.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]
        return "\n".join(lines[:10])

    def cmd_tac(self, args):
        """Вывести содержимое файла в обратном порядке строк"""
        if not args:
            return "tac: missing file operand"

        content, error = self.vfs.get_file_content(self.vfs.resolve_path(args[0]))
        if error:
            return f"tac: {error}"

        lines = content.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]
        return "\n".join(reversed(lines))

    def cmd_rev(self, args):
        """Вывести содержимое файла с обратным порядком символов в строках"""
        if not args:
            return "rev: missing file operand"

        content, error = self.vfs.get_file_content(self.vfs.resolve_path(args[0]))
        if error:
            return f"rev: {error}"

        lines = content.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]

        reversed_lines = [line[::-1] for line in lines]
        return "\n".join(reversed_lines)

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