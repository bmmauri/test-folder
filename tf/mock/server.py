import logging
import pickle
import socketserver
import tf
import tf.core.engine as engine
import threading
import time

logger = logging.getLogger("TestFolder")


class MockSocketHandler(socketserver.BaseRequestHandler):
    """
    Simple handler for Mock server.
    TODO:
        - could be customizable?
    """

    def handle(self) -> None:
        self.data = self.request.recv(1024).strip()
        self.request.sendall(self.data.upper())


class MockSocketStateHandler(socketserver.BaseRequestHandler):
    """
    Simple states handler for Mock server.
    """

    def _transition(self):
        machine = self.server._action.get_machine()
        machine_operation = getattr(machine, self.data.__class__.__name__.lower())
        if callable(machine_operation):
            machine_operation()
        else:
            raise AttributeError(
                "Please provide an existing operation."
            )

    def handle(self) -> None:
        self.data = pickle.loads(self.request.recv(1024))
        self._transition()
        self.request.sendall(
            bytes(str('Transition ..'), encoding='utf-8')
        )


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
        socketserver.TCPServer.allow_reuse_address = True
        self._action = tf.Action()
        super().__init__((host, port), handler, bind_and_activate=False)

    def __run(self):
        host, port = self.server_address
        logger.debug(f"TCPServer running at tcp://{host}:{port}")
        with self as server:
            server.server_bind()
            server.server_activate()
            server.serve_forever()

    def __finish(self):
        logger.debug("Server is finishing..")
        counter = 20
        while self._action.get_machine().machine_state == engine.MachineState.PAUSE:
            if counter == 0:
                logger.warning(f"Machine forced to finish")
                break
            logger.warning(f"MachineState: {engine.MachineState.PAUSE.name} need to be terminated")
            time.sleep(0.5)
            counter -= 1
            continue

        self._action.get_machine().finish()
        self.shutdown()

    def _wait_until_close(self):
        while not self.socket._closed:
            time.sleep(0.5)
            continue

    def fork_until(self, interval: int = 5, detach: bool = False):
        threading.Thread(target=self.__run).start()
        machine = self._action.get_machine()
        if machine:
            machine.run()
        if not detach:
            time.sleep(interval)
            self.__finish()
        else:
            threading.Timer(interval=interval, function=self.__finish).start()
