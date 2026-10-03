"""Точка входа в приложение эмулятора оболочки"""

import argparse

from src.gui import ShellGUI


def parse_arguments():
    """Разобрать аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки UNIX-подобной ОС"
    )
    parser.add_argument(
        "--vfs",
        help="Путь к физическому расположению VFS",
        default=None
    )
    parser.add_argument(
        "--script",
        help="Путь к стартовому скрипту",
        default=None
    )
    return parser.parse_args()


def main():
    """Запустить эмулятор оболочки с учетом аргументов."""
    args = parse_arguments()
    app = ShellGUI(
        vfs_name="VFS",
        vfs_path=args.vfs,
        script_path=args.script
    )
    app.run()


if __name__ == "__main__":
    main()