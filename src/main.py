"""Точка входа в приложение эмулятора оболочки"""

from src.gui import ShellGUI


def main():
    """Запустить эмулятор оболочки"""
    app = ShellGUI()
    app.run()


if __name__ == "__main__":
    main()