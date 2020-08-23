import pickle
import socketserver
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


class MockSocketStateHandler(socketserver.BaseRequestHandler):
    """
    Simple states handler for Mock server.
    """

    def handle(self) -> None:
        self.data = pickle.loads(self.request.recv(1024))
        print(str(self.data))
        self.request.sendall(bytes(str(self.data), encoding='utf-8'))


class MockTCPServer(socketserver.TCPServer):
    """
    Simple TCP Mock server.
    """
    _action = None

    def __init__(self, host: str = 'localhost', port: int = 8888, handler=MockSocketHandler):
        """Socket server easy object (Mock).

        :param host: hostname to expose
        :param port: port to expose
        :param handler: Handler object that handle response for each client call
        """
        self._action = tf.Action()
        super().__init__((host, port), handler, bind_and_activate=False)

    def __run(self):
        host, port = self.server_address
        print(f"TCPServer running at tcp://{host}:{port}")
        with self as server:
            server.server_bind()
            server.server_activate()
            server.serve_forever()

    def __close(self):
        self._action.get_machine().finish()
        self.shutdown()

    def fork_until(self, interval: int = 5, detach: bool = False):
        threading.Thread(target=self.__run).start()
        machine = self._action.get_machine()
        if machine:
            machine.run()
        if not detach:
            time.sleep(interval)
            self.__close()
        else:
            threading.Timer(interval=interval, function=self.__close).start()
