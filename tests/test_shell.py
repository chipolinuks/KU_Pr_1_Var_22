"""Тесты для модуля оболочки"""

import unittest
from src.shell import Shell


class TestShellParser(unittest.TestCase):
    """Тесты парсера команд"""

    def setUp(self):
        """Создать экземпляр оболочки"""
        self.shell = Shell()

    def test_simple_command(self):
        """Тест простой команды без аргументов"""
        cmd, args, error = self.shell.parse_command("ls")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, [])
        self.assertIsNone(error)

    def test_command_with_args(self):
        """Тест команды с аргументами"""
        cmd, args, error = self.shell.parse_command("ls -la /home")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["-la", "/home"])
        self.assertIsNone(error)

    def test_quoted_args(self):
        """Тест аргументов в кавычках"""
        cmd, args, error = self.shell.parse_command('ls "my folder"')
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["my folder"])
        self.assertIsNone(error)

    def test_empty_line(self):
        """Тест пустой строки"""
        cmd, args, error = self.shell.parse_command("   ")
        self.assertIsNone(cmd)
        self.assertIsNone(error)

    def test_invalid_quotes(self):
        """Тест некорректных кавычек"""
        cmd, args, error = self.shell.parse_command('ls "unclosed')
        self.assertIsNone(cmd)
        self.assertIsNotNone(error)
        self.assertIn("кавычки", error)


class TestShellCommands(unittest.TestCase):
    """Тесты команд оболочки"""

    def setUp(self):
        """Создать экземпляр оболочки"""
        self.shell = Shell()

    def test_ls_stub(self):
        """Тест заглушки ls"""
        result = self.shell.execute("ls", ["hi"])
        self.assertEqual(result, "ls: ['hi']")

    def test_cd_stub(self):
        """Тест заглушки cd"""
        result = self.shell.execute("cd", ["hello"])
        self.assertEqual(result, "cd: ['hello']")

    def test_exit_command(self):
        """Тест команды exit"""
        result = self.shell.execute("exit", [])
        self.assertIn("Выход", result)
        self.assertFalse(self.shell.is_running())

    def test_unknown_command(self):
        """Тест неизвестной команды"""
        result = self.shell.execute("unknown", [])
        self.assertIn("Ошибка", result)


if __name__ == "__main__":
    unittest.main()