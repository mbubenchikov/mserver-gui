import asyncio
import threading

from server_runner import ServerRunner
from gui import GUI


def main():
    server_runner = ServerRunner()
    gui = GUI(lambda self: start(server_runner),
              lambda self: stop(server_runner, self),
              lambda self, command: input(server_runner, command),
              lambda self: close(server_runner, self))

    server_runner.new_line_action = gui.new_line_action

    gui.show()


def start(server_runner: ServerRunner):
    threading.Thread(target=asyncio.run, args=(server_runner.run(),)).start()


def stop(server_runner: ServerRunner, gui: GUI):
    if server_runner.is_working:
        server_runner.stop()
    else:
        gui.show_message("Stop", "Server is already stopped!")


def close(server_runner: ServerRunner, gui: GUI):
    if server_runner.is_working:
        if gui.show_message("Exit", "Do you want to exit?"):
            server_runner.stop()  # TODO: async
            gui.close()
    else:
        gui.close()


def input(server_runner: ServerRunner, command: str):
    server_runner.input(command)


if __name__ == '__main__':
    main()
