import json
import logging
import msgpack
import os
import pickle
import pty
import serial
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
        machine.server.set_data(self.data)
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

    def _run(self):
        host, port = self.server_address
        logger.debug(f"TCPServer running at tcp://{host}:{port}")
        with self as server:
            server.server_bind()
            server.server_activate()
            server.serve_forever()

    def _finish(self):
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
        threading.Thread(target=self._run).start()
        machine = self._action.get_machine()
        if machine:
            machine.run()
        if not detach:
            time.sleep(interval)
            self._finish()
        else:
            threading.Timer(interval=interval, function=self._finish).start()


class RoboticMockTCPServer(MockTCPServer):
    """Robotic server (Mock)."""

    __servos_position = {
        "s1": 0, "s2": 0, "s3": 0,
        "s4": 0, "s5": 0, "s6": 0
    }
    __master_fd, __slave_fd = None, None
    __serial_device_name = None
    __board: serial.Serial = None
    __data = None

    def __init__(self, host: str = 'localhost', port: int = 8888, handler=MockSocketStateHandler):
        super().__init__(host, port, handler)
        self.__virtual_serial_device()

    def __virtual_serial_device(self):
        self.__master_fd, self.__slave_fd = pty.openpty()
        self.__serial_device_name = os.ttyname(self.__slave_fd)
        self.__board = serial.Serial(port=self.__serial_device_name)
        logger.debug(f"Virtual Serial Device '{self.__serial_device_name}' is open")

    def get_servos_position(self): return self.__servos_position

    def set_data(self, _data):
        self.__data = _data

    def get_data(self):
        return self.__data

    def update(self, positions: dict = None):
        positions = positions if positions is not None else {}
        self.__servos_position.update(positions)

    def init(self):
        self._calibrate()
        self._action.get_machine().ready()

    def _calibrate(self):
        self._action.get_machine().not_ready()
        self.do()

    def do(self):
        logger.warning('Robot is working')
        if not self.__board:
            raise SystemError("There is no board available")
        byte_message = msgpack.packb(self.__servos_position, use_bin_type=True)
        logger.warning("Update servos position")
        logger.info(json.dumps(self.__servos_position, indent=2))
        self.__board.write(byte_message)
