import tkinter as tk
from tkinter import messagebox
import asyncio
import threading

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    pass

from shell import ServerShell

window = tk.Tk()

shell = ServerShell()

def main():
    button_start = tk.Button(
        text="RUN",
        width=15,
        height=5,
        bg="black",
        fg="white",
    )

    button_stop = tk.Button(
        text="STOP",
        width=15,
        height=5,
        bg="black",
        fg="white",
    )

    button_help = tk.Button(
        text="HELP",
        width=15,
        height=5,
        bg="black",
        fg="white",
    )

    entry = tk.Entry()

    button_start.bind("<Button-1>", lambda event: handle_start())
    button_stop.bind('<Button-1>', lambda event: handle_stop())
    button_help.bind('<Button-1>', lambda event: handle_help())
    window.protocol("WM_DELETE_WINDOW", lambda: handle_close())

    button_start.pack()
    button_stop.pack()
    button_help.pack()
    entry.pack()

    window.mainloop()


def handle_start():
    threading.Thread(target=asyncio.run, args=(shell.start(),)).start()


def handle_help():
    if shell.server_working:
        shell.input('help')
    else:
        messagebox.showinfo("Help", "Server is stopped!")


def handle_stop():
    if shell.server_working:
        shell.stop()
    else:
        messagebox.showinfo("Stop", "Server is already stopped!")


def handle_close():
    if shell.server_working:
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            shell.stop()  # TODO: async
            window.destroy()
    else:
        window.destroy()


if __name__ == '__main__':
    main()
