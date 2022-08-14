import asyncio
from asyncio.subprocess import Process
from os import path as os_path, makedirs
from typing import Optional
from datetime import datetime


class ServerShell:
    def __init__(self):
        self._process: Optional[Process] = None
        self._queue: Optional[asyncio.Queue] = None
        self._event_loop = None
        self.server_working = False

        makedirs(os_path.join(os_path.dirname(__file__), './data'), exist_ok=True)

    async def start(self):
        self._event_loop = asyncio.get_running_loop()
        self._queue = asyncio.Queue()

        self._process = await asyncio.create_subprocess_exec("java", "-Xmx4092M", "-Xms1024M", "-jar", "../server.jar", "nogui",
                                                             cwd=os_path.join(os_path.dirname(__file__), './data'),
                                                             stdout=asyncio.subprocess.PIPE,
                                                             stdin=asyncio.subprocess.PIPE)

        self.server_working = True

        read_output_task = asyncio.create_task(self._read_output())
        wait_for_input_task = asyncio.create_task(self._wait_for_input())

        await self._process.wait()
        self.server_working = False

        read_output_task.cancel()
        wait_for_input_task.cancel()

    def stop(self):
        self.input("stop")

    def input(self, command: str):
        print(f"> {command}")
        asyncio.run_coroutine_threadsafe(self._queue.put(command), self._event_loop)

    async def _read_output(self):
        while line := await self._process.stdout.readline():
            print(line.rstrip().decode(errors='ignore'))

    async def _write_input(self, command: str):
        byte_command = command.encode() + b'\n'
        self._process.stdin.write(byte_command)
        await self._process.stdin.drain()

    async def _wait_for_input(self):
        while True:
            command = await self._queue.get()
            await self._write_input(command)
            self._queue.task_done()
