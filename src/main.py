"""Графический терминал учебной виртуальной оболочки."""

import argparse
from pathlib import Path
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


def start_script(terminal, path):
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, ValueError) as error:
        terminal.write(f"Ошибка чтения сценария: {error}")
        return

    def step(index):
        if index < len(lines):
            terminal.run(lines[index], f"{path}:{index + 1}")
            if not terminal.shell.closed:
                terminal.root.after(100, step, index + 1)

    step(0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vfs", type=Path)
    parser.add_argument("--script", type=Path)
    args = parser.parse_args()
    try:
        shell = Shell(args.vfs)
    except ValueError as error:
        parser.exit(1, f"{error}\n")
    root = tk.Tk()
    terminal = Terminal(root, shell)
    terminal.write(f"vfs={args.vfs}, script={args.script}")
    if args.script:
        root.after(100, start_script, terminal, args.script)
    root.mainloop()


if __name__ == "__main__":
    main()
