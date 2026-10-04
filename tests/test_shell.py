"""Тесты для модуля оболочки"""

import unittest
from src.shell import Shell


class TestShellParser(unittest.TestCase):
    """Тесты парсера команд"""

    def setUp(self):
        """Создать оболочку перед каждым тестом"""
        self.shell = Shell()

    def test_simple_command(self):
        """Простая команда без аргументов"""
        command, args, error = self.shell.parse_command("ls")
        self.assertEqual(command, "ls")
        self.assertEqual(args, [])
        self.assertIsNone(error)

    def test_command_with_args(self):
        """Команда с аргументами"""
        command, args, error = self.shell.parse_command("cd home")
        self.assertEqual(command, "cd")
        self.assertEqual(args, ["home"])
        self.assertIsNone(error)

    def test_quoted_args(self):
        """Аргументы в кавычках"""
        command, args, error = self.shell.parse_command('cd "my folder"')
        self.assertEqual(command, "cd")
        self.assertEqual(args, ["my folder"])
        self.assertIsNone(error)

    def test_empty_line(self):
        """Пустая строка"""
        command, args, error = self.shell.parse_command("")
        self.assertIsNone(command)
        self.assertIsNone(args)
        self.assertIsNone(error)

    def test_invalid_quotes(self):
        """Незакрытые кавычки"""
        command, args, error = self.shell.parse_command('ls "foo')
        self.assertIsNone(command)
        self.assertIsNotNone(error)


class TestShellCommands(unittest.TestCase):
    """Тесты команд оболочки"""

    def setUp(self):
        """Создать оболочку перед каждым тестом"""
        self.shell = Shell()

    def test_unknown_command(self):
        """Неизвестная команда"""
        result = self.shell.execute("foobar", [])
        self.assertIn("неизвестная команда", result)

    def test_exit_command(self):
        """Команда exit"""
        result = self.shell.execute("exit", [])
        self.assertIn("Выход", result)
        self.assertFalse(self.shell.is_running())

    def test_ls_root(self):
        """ls в корневой директории"""
        result = self.shell.execute("ls", [])
        self.assertIsInstance(result, str)

    def test_cd_nonexistent(self):
        """cd в несуществующую директорию"""
        result = self.shell.execute("cd", ["nonexistent"])
        self.assertIn("no such file or directory", result)

    def test_cd_root(self):
        """cd в корень"""
        result = self.shell.execute("cd", ["/"])
        self.assertEqual(result, "")
        self.assertEqual(self.shell.vfs.current_path, "/")

    def test_ls_nonexistent(self):
        """ls несуществующего пути"""
        result = self.shell.execute("ls", ["nonexistent"])
        self.assertIn("No such file or directory", result)


class TestShellWithVFS(unittest.TestCase):
    """Тесты команд с загруженной VFS"""

    def setUp(self):
        """Создать оболочку с тестовой VFS"""
        self.shell = Shell(vfs_path="data/vfs_minimal.json")

    def test_ls_with_vfs(self):
        """ls с загруженной VFS"""
        result = self.shell.execute("ls", [])
        self.assertIsInstance(result, str)

    def test_cd_valid_path(self):
        """cd в существующую директорию"""
        result = self.shell.execute("cd", ["/"])
        self.assertEqual(result, "")

    def test_head_command(self):
        """Команда head"""
        result = self.shell.execute("head", [])
        self.assertIn("missing file operand", result)

    def test_tac_command(self):
        """Команда tac"""
        result = self.shell.execute("tac", [])
        self.assertIn("missing file operand", result)

    def test_rev_command(self):
        """Команда rev"""
        result = self.shell.execute("rev", [])
        self.assertIn("missing file operand", result)


if __name__ == "__main__":
    unittest.main()