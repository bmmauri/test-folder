"""
Engine module
    - Machine object
"""
import enum

from typing import Union

from tf.mock.client import MockTCPClient
from tf.mock.server import MockTCPServer


class MachineState(enum.Enum):
    ABORT = 0
    INIT = 1
    START = 2
    RUN = 3
    PAUSE = 4
    BLOCK = 5
    FINISH = 6
    COMPLETE = 7
    CLOSE = 8


class Machine:

    def __init__(self) -> None:
        """Machine base object."""
        self._collections: set = set()
        self._actions: set = set()
        self._machine_state: Union[None, int] = None
        self.init()

    def attach(self, action):
        action._machine = self
        self._actions.add(action)

    def detach(self, action):
        action._machine = None
        self._actions.discard(action)

    def _notify(self):
        for action in self._actions:
            action.update(self._machine_state)

    def abort(self): self.machine_state = MachineState.ABORT

    def init(self): self.machine_state = MachineState.INIT

    def start(self): self.machine_state = MachineState.START

    def run(self): self.machine_state = MachineState.RUN

    def pause(self): self.machine_state = MachineState.PAUSE

    def block(self): self.machine_state = MachineState.BLOCK

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


class HttpMachine(Machine):

    def __init__(self):
        super().__init__()
