"""
Engine module
    - Machine object
"""
import enum
import json
import logging

from typing import Union

from tf import utils
from tf.mock.client import MockTCPClient
from tf.mock.server import MockTCPServer, MockSocketStateHandler, RoboticMockTCPServer

logger = logging.getLogger()
handler = logging.FileHandler(filename=f"{logger.name}.log", mode="w")
handler.setFormatter(utils.Formatter())
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class MachineState(enum.Enum):
    ABORT = 0
    INIT = 1
    READY = 2
    NOT_READY = 3
    START = 4
    RUN = 5
    PAUSE = 6
    BLOCK = 7
    FINISH = 8
    COMPLETE = 9
    CLOSE = 10


class Machine:

    def __init__(self) -> None:
        """Machine base object."""
        self._collections: set = set()
        self._actions: set = set()
        self._machine_state: Union[None, MachineState] = None
        self.init()
        self.ready()

    def attach(self, action):
        action._machine = self
        self._actions.add(action)

    def detach(self, action):
        action._machine = None
        self._actions.discard(action)

    def _notify(self):
        logger.debug(f'Notice machine state: {self.machine_state.name}')
        for action in self._actions:
            action.update(self._machine_state)

    def abort(self):
        logger.error("Please checked out the machine")
        self.machine_state = MachineState.ABORT

    def init(self): self.machine_state = MachineState.INIT

    def ready(self): self.machine_state = MachineState.READY

    def not_ready(self): self.machine_state = MachineState.NOT_READY

    def start(self): self.machine_state = MachineState.START

    def run(self): self.machine_state = MachineState.RUN

    def pause(self): self.machine_state = MachineState.PAUSE

    def block(self):
        logger.error("Please checked out the machine")
        self.machine_state = MachineState.BLOCK

    def finish(self): self.machine_state = MachineState.FINISH

    def complete(self): self.machine_state = MachineState.COMPLETE

    def close(self): self.machine_state = MachineState.CLOSE

    @property
    def machine_state(self):
        return self._machine_state

    @machine_state.setter
    def machine_state(self, arg):
        self._machine_state = arg
        self._notify()


class SocketMachine(Machine):

    def __init__(self, client: MockTCPClient, server: MockTCPServer):
        """Argument to instance a Socket machine

        :param client: client object
        :param server: server object
        """
        super().__init__()
        self._client = client
        self._server = server
        self._collections.add(self._client)
        self._collections.add(self._server)
        self.__attach()

    @property
    def client(self):
        return self._client

    @property
    def server(self):
        return self._server

    def close(self):
        self.server.shutdown()
        super().close()

    def __attach(self):
        for element in self._collections:
            if hasattr(element, '_action'):
                super().attach(getattr(element, '_action'))
        self.start()


class RoboticMachine(Machine):
    debug: bool = False

    __microprocessor = {
        "ip": "192.168.4.2", "port": 80, "uri": "/servo/"
    }

    def __init__(self, client: MockTCPClient):
        """Argument to instance a Socket machine

        :param client: client object
        """
        super().__init__()
        self._client = client
        self._server = RoboticMockTCPServer()
        self._collections.add(self._client)
        self._collections.add(self._server)
        self.__attach()
        self._server.init()

    @property
    def client(self):
        return self._client

    @property
    def server(self):
        return self._server

    @property
    def microprocessor(self):
        return self.__microprocessor

    def close(self):
        self.server.shutdown()
        super().close()

    def __attach(self):
        for element in self._collections:
            if hasattr(element, '_action'):
                super().attach(getattr(element, '_action'))

    def __parse_current_command(self):
        return json.loads(self._server.get_data().get_command())

    def run(self):
        super().run()
        content = self.__parse_current_command()
        self._server.update(content)
        logger.warning('Writing on robot..')
        logger.info(json.dumps(self._server.get_servos_position(), indent=2))
        if not self.debug:
            self._server.do()


class HttpMachine(Machine):

    def __init__(self):
        super().__init__()
