import tkinter as tk
from tkinter import messagebox
from typing import Callable

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    pass


class GUI:
    def __init__(self, start_func: Callable[['GUI'], None],
                 stop_func: Callable[['GUI'], None],
                 input_func: Callable[['GUI', str], None],
                 close_func: Callable[['GUI'], None]):
        self.start_func = start_func
        self.stop_func = stop_func
        self.input_func = input_func
        self.close_func = close_func

        self.root = tk.Tk()

        text_box = tk.Text(self.root, height=30, width=100)
        text_box.yview_scroll(1, "units")
        text_box.yview('end')
        text_box.see("end")

        entry = tk.Entry(width=100)
        entry.bind('<Return>', lambda event: self._input_text(entry))

        button_start = tk.Button(text="RUN", width=10, height=5, bg="black", fg="white")
        button_stop = tk.Button(text="STOP", width=10, height=5, bg="black", fg="white")
        button_start.bind("<Button-1>", lambda event: self.start_func(self))
        button_stop.bind('<Button-1>', lambda event: self.stop_func(self))

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_func(self))

        self.new_line_action = lambda s: self._show_line(s, text_box)

        text_box.pack()
        entry.pack()
        button_start.pack()
        button_stop.pack()

    def show(self):
        self.root.mainloop()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def close(self):
        self.root.destroy()

    def _input_text(self, entry: tk.Entry):
        self.input_func(self, entry.get())
        entry.delete(0, tk.END)

    def _show_line(self, line: str, text_box: tk.Text):
        text_box.insert('end', f'{line}\n')
        text_box.see('end')
