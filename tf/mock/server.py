import json
import logging
import msgpack
import os
import pickle
import pty
import requests
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
            machine.start()
        if not detach:
            time.sleep(interval)
            self._finish()
        else:
            threading.Timer(interval=interval, function=self._finish).start()


class RoboticMockTCPServer(MockTCPServer):
    """Robotic server (Mock)."""

    __servos_position = {
        "s0": 130, "s1": None,
        "s2": None, "s3": None,
        "s4": None, "s5": None, "s6": None
    }
    __data = None

    def __init__(self, host: str = 'localhost', port: int = 8888, handler=MockSocketStateHandler):
        super().__init__(host, port, handler)

    def get_servos_position(self):
        return self.__servos_position

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
        time.sleep(5)

    def do(self):
        logger.warning('Robot engagement')
        msgpack.packb(self.__servos_position, use_bin_type=True)
        microprocessor = self._action.get_machine().microprocessor
        base_url = f"http://" \
                   f"{microprocessor.get('ip', None)}" \
                   f":{microprocessor.get('port', None)}" \
                   f"{microprocessor.get('uri', None)}"
        for servo, pos in self.__servos_position.items():
            if pos is not None:
                endpoint = f"{base_url}{servo}/{pos}"
                requests.get(endpoint)
                time.sleep(1)
        logger.warning("Update servos position")
        logger.warning(self.__servos_position)
