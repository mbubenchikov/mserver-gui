import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter.font as tkFont
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
        self.root.minsize(1500, 700)

        console_frame = tk.Frame(self.root)
        font = tkFont.Font(family='Courier New', weight='bold')
        text_box = scrolledtext.ScrolledText(console_frame)
        text_box.configure(font=font)

        entry = tk.Entry(console_frame)
        entry.bind('<Return>', lambda event: self._input_text(entry))
        entry.configure(font=font)

        controls_frame = tk.Frame(self.root)
        buttons_frame = tk.Frame(controls_frame)
        button_start = tk.Button(buttons_frame, text="RUN", width=15)
        button_stop = tk.Button(buttons_frame, text="STOP", width=15)
        button_start.bind("<Button-1>", lambda event: self.start_func(self))
        button_stop.bind('<Button-1>', lambda event: self.stop_func(self))

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_func(self))

        self.new_line_action = lambda s: self._show_line(s, text_box)

        console_frame.pack(side='left', fill='both', expand=True)
        controls_frame.pack(side='right', fill='y')
        buttons_frame.pack(side='bottom')
        text_box.pack(side='top', fill='both', expand=True)
        entry.pack(side='bottom', fill='x')
        button_start.pack(side='left')
        button_stop.pack(side='right')

    def show(self):
        self.root.mainloop()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def ask(self, title, message):
        return messagebox.askokcancel(title, message)

    def close(self):
        self.root.destroy()

    def _input_text(self, entry: tk.Entry):
        self.input_func(self, entry.get())
        entry.delete(0, tk.END)

    def _show_line(self, line: str, text_box: tk.Text):
        text_box.configure(state='normal')
        text_box.insert('end', f'\n{line}')
        text_box.see('end')
        text_box.configure(state='disabled')
