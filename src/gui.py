"""Модуль графического интерфейса эмулятора"""

import tkinter as tk
from src.shell import Shell


class ShellGUI:
    """Класс графического интерфейса оболочки"""

    def __init__(self, vfs_name="VFS", vfs_path=None, script_path=None):
        """Инициализировать GUI"""
        self.root = tk.Tk()
        self.root.title(f"Эмулятор - {vfs_name}")
        self.root.geometry("700x500")
        self.root.minsize(500, 400)

        self.shell = Shell(vfs_path=vfs_path)

        self._create_widgets()

        self._append_output("=== Отладочная информация ===")
        self._append_output(f"Путь к VFS: {vfs_path if vfs_path else 'не задан'}")
        self._append_output(f"Путь к скрипту: {script_path if script_path else 'не задан'}")
        self._append_output(self.shell.vfs_load_message)
        self._append_output("=============================")

        if script_path:
            self._run_startup_script(script_path)

    def _create_widgets(self):
        """Создать элементы интерфейса"""
        self.output_frame = tk.Frame(self.root, bg="white")
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_text = tk.Text(
            self.output_frame,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="black",
            fg="white",
            insertbackground="white"
        )
        scrollbar = tk.Scrollbar(
            self.output_frame,
            command=self.output_text.yview
        )
        self.output_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.prompt_label = tk.Label(
            self.input_frame,
            text="$ ",
            font=("Consolas", 10),
            fg="green"
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(
            self.input_frame,
            font=("Consolas", 10),
            bd=1,
            relief=tk.SOLID
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.input_entry.bind("<Return>", self._on_enter)
        self.root.after(100, self.input_entry.focus_set)

    def _on_enter(self, event):
        """Обработать нажатие Enter"""
        line = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self._append_output(f"$ {line}")

        command, args, error = self.shell.parse_command(line)

        if error is not None:
            self._append_output(error)
            return

        if command is None:
            return

        result = self.shell.execute(command, args)
        self._append_output(result)

        if not self.shell.is_running():
            self.root.after(1000, self.root.destroy)

    def _append_output(self, text):
        """Добавить текст в область вывода"""
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def _run_startup_script(self, script_path):
        """Выполнить стартовый скрипт"""
        self._append_output(f"\n--- Запуск скрипта: {script_path} ---")
        results = self.shell.run_script(script_path)
        for line, result in results:
            self._append_output(f"$ {line}")
            self._append_output(result)
            self.root.update()
        self._append_output("--- Скрипт завершен ---\n")

    def run(self):
        """Запустить главный цикл GUI"""
        self.root.mainloop()