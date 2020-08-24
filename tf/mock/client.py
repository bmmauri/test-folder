import logging
import socket
import tf

from typing import Union


class MockTCPClient(socket.socket):
    _action = None

    def __init__(self, host: str = "localhost", port: int = 8888) -> None:
        """Argument needed to connect to server.

        :param host: hostname of the server
        :param port: port of the server
        """
        self._action = tf.Action()
        super().__init__()
        self._ADDRESS = host, port

    def _quit(self):
        self._action.get_machine().abort()
        self._action.get_machine().detach(self._action)

    def call(self, message: Union[None, str, bytes] = None):
        with self as sock:
            try:
                sock.connect(self._ADDRESS)
            except Exception as e:
                logging.exception(e)
                self._quit()
                raise e
            if type(message) is bytes:
                sock.send(message)
            else:
                sock.send(bytes(message, encoding='utf-8'))
            return str(sock.recv(1024), encoding="utf-8")
