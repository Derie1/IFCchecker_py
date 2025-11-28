import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import subprocess
import threading
import sys
import os


class IFCCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IFC Checker GUI")

        self.process = None  # будем хранить процесс мониторинга

        # Поле выбора папки
        self.folder_label = tk.Label(root, text="Monitoring folder:")
        self.folder_label.pack(anchor="w", padx=10, pady=5)

        self.folder_entry = tk.Entry(root, width=50)
        self.folder_entry.pack(side="left", padx=10, pady=5)

        self.browse_button = tk.Button(
            root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="left", padx=5, pady=5)

        # Выбор языка
        self.lang_label = tk.Label(root, text="Language:")
        self.lang_label.pack(anchor="w", padx=10, pady=5)

        self.lang_var = tk.StringVar(value="en")
        self.lang_combo = ttk.Combobox(root, textvariable=self.lang_var,
                                       values=["en", "ru", "de"], width=10)
        self.lang_combo.pack(anchor="w", padx=10, pady=5)

        # Кнопки запуска и остановки
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(padx=10, pady=10)

        self.start_button = tk.Button(
            self.button_frame, text="Start monitoring", command=self.start_monitoring)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(
            self.button_frame, text="Stop monitoring", command=self.stop_monitoring, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        # Поле для отображения сообщений
        self.output_text = scrolledtext.ScrolledText(
            root, width=80, height=20, state="disabled")
        self.output_text.pack(padx=10, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def start_monitoring(self):
        folder = self.folder_entry.get()
        lang = self.lang_var.get()

        if not folder:
            self.append_output("Please select a folder first.\n")
            return

        # Запускаем IFC_checker.py как отдельный процесс
        def run_checker():
            self.process = subprocess.Popen(
                [sys.executable, "IFC_checker.py", folder, "--lang", lang],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            for line in self.process.stdout:
                self.append_output(line)
            self.process.stdout.close()
            self.process.wait()
            self.append_output("Monitoring stopped.\n")

        threading.Thread(target=run_checker, daemon=True).start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_monitoring(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()  # корректно завершаем процесс
            self.append_output("Stopping monitoring...\n")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def append_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = IFCCheckerGUI(root)
    root.mainloop()
