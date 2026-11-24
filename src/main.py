"""Графический терминал учебной виртуальной оболочки."""

import getpass
import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from shell import Shell


class Terminal:
    def __init__(self, root, shell):
        self.root = root
        self.shell = shell
        root.title(f"Эмулятор — [{getpass.getuser()}@{socket.gethostname()}]")
        self.history = ScrolledText(root, width=80, height=23, state="disabled")
        self.history.pack(fill="both", expand=True)
        self.entry = tk.Entry(root)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()

    def write(self, text):
        self.history.configure(state="normal")
        self.history.insert("end", text + "\n")
        self.history.see("end")
        self.history.configure(state="disabled")

    def run(self, line, location=""):
        self.write(f"{self.shell.cwd}$ {line}")
        try:
            result = self.shell.execute(line)
            if result:
                self.write(result.removesuffix("\n"))
        except ValueError as error:
            self.write(f"Ошибка {location}: {error}")
        if self.shell.closed:
            self.root.destroy()

    def submit(self, event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.run(line)


def main():
    root = tk.Tk()
    Terminal(root, Shell())
    root.mainloop()


if __name__ == "__main__":
    main()
