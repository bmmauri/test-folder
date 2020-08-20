import socketserver
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

    def __init__(self, host: str = 'localhost', port: int = 8888, handler=None):
        super().__init__((host, port), handler, bind_and_activate=False)

    def run(self):
        host, port = self.server_address
        print(f"TCPServer running at tcp://{host}:{port}")
        with self as server:
            server.server_bind()
            server.server_activate()
            server.serve_forever()

    def fork_until(self, _method, interval: int = 5):
        if not callable(_method):
            raise SystemError("Need to be passed a callable method")
        threading.Timer(interval=1, function=_method).start()
        time.sleep(interval)
        self.shutdown()

