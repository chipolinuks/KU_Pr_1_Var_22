"""Модуль оболочки эмулятора"""

import shlex


class Shell:
    """Класс оболочки эмулятора командной строки"""

    def __init__(self):
        """Инициализация оболочки"""
        self.running = True
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
        """Заглушка команды ls"""
        return f"ls: {args}"

    def cmd_cd(self, args):
        """Заглушка команды cd"""
        return f"cd: {args}"

    def cmd_exit(self, args):
        """Команда выхода из оболочки"""
        self.running = False
        return "Выход из эмулятора."

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