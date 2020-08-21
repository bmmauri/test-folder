import socket
import socketserver
from typing import Union

import tf
import threading
import time


class MockSocketHandler(socketserver.BaseRequestHandler):
    """
    Simple handler for Mock server.
    TODO:
        - could be customizable?
    """

    def handle(self) -> None:
        self.data = self.request.recv(1024).strip()
        print(self.data)
        self.request.sendall(self.data.upper())


class MockTCPServer(socketserver.TCPServer):
    """
    Simple TCP Mock server.
    """
    _action = None

    def __init__(self, host: str = 'localhost', port: int = 8888, handler=MockSocketHandler):
        super().__init__((host, port), handler, bind_and_activate=False)

    def __run(self):
        host, port = self.server_address
        print(f"TCPServer running at tcp://{host}:{port}")
        with self as server:
            server.server_bind()
            server.server_activate()
            server.serve_forever()

    def fork_until(self, interval: int = 5, detach: bool = False):
        run = threading.Thread(target=self.__run).start()
        if not detach:
            time.sleep(interval)
            self.shutdown()
        else:
            shutdown = threading.Timer(interval=interval, function=self.shutdown).start()

    def set_action(self, action):
        self._action = action


class SocketClient(socket.socket):
    _action = None

    def __init__(self, host: str = "localhost", port: int = 8888) -> None:
        super().__init__()
        self._ADDRESS = host, port

    def call(self, message: Union[None, str] = None):
        with self as sock:
            sock.connect(self._ADDRESS)
            sock.send(bytes(message, encoding='utf-8'))
            return str(sock.recv(1024), encoding="utf-8")

    def set_action(self, action):
        self._action = action
