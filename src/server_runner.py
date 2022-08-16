import asyncio
from asyncio.subprocess import Process
from os import path as os_path, makedirs
from typing import Optional, Callable


class ServerRunner:
    def __init__(self):
        self._process: Optional[Process] = None
        self._queue: Optional[asyncio.Queue] = None
        self._event_loop: Optional[asyncio.BaseEventLoop] = None
        self._is_working: bool = False

        self.new_line_action: Optional[Callable[[str], None]] = None

        makedirs(os_path.join(os_path.dirname(__file__), './data'), exist_ok=True)

    async def run(self):
        self._event_loop = asyncio.get_running_loop()
        self._queue = asyncio.Queue()

        self._process = await asyncio.create_subprocess_exec("java", "-Xmx4092M", "-Xms1024M", "-jar", "../server.jar", "nogui",
                                                             cwd=os_path.join(os_path.dirname(__file__), './data'),
                                                             stdout=asyncio.subprocess.PIPE,
                                                             stdin=asyncio.subprocess.PIPE)

        self._is_working = True

        read_output_task = asyncio.create_task(self._read_output())
        wait_for_input_task = asyncio.create_task(self._wait_for_input())

        await self._process.wait()

        read_output_task.cancel()
        wait_for_input_task.cancel()

        self._reset()

    def stop(self):
        self.input("stop")

    def input(self, command: str):
        if self._event_loop:
            asyncio.run_coroutine_threadsafe(self._queue.put(command), self._event_loop)

    @property
    def is_working(self):
        return self._is_working

    def _reset(self):
        self._process: Optional[Process] = None
        self._queue: Optional[asyncio.Queue] = None
        self._event_loop = None
        self._is_working = False

    async def _read_output(self):
        while line := await self._process.stdout.readline():
            if self.new_line_action:
                self.new_line_action(line.rstrip().decode(errors='ignore'))

    async def _write_input(self, command: str):
        byte_command = command.encode() + b'\n'
        self._process.stdin.write(byte_command)
        await self._process.stdin.drain()

    async def _wait_for_input(self):
        while True:
            command = await self._queue.get()
            await self._write_input(command)
            if self.new_line_action:
                self.new_line_action(command)
            self._queue.task_done()
