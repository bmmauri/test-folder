"""
Engine module
    - Machine object
"""
import abc
import enum
import socket

from typing import Union


class MachineState(enum.Enum):
    ABORT = 0
    START = 1
    RUN = 2
    PAUSE = 3
    BLOCK = 4
    FINISH = 5


class Machine:

    def __init__(self):
        self._collections: set = set()
        self._actions: set = set()
        self._machine_state: Union[None, int] = None

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

    def start(self): self.machine_state = MachineState.START

    def run(self): self.machine_state = MachineState.RUN

    def pause(self): self.machine_state = MachineState.PAUSE

    def block(self): self.machine_state = MachineState.BLOCK

    def finish(self): self.machine_state = MachineState.FINISH

    @property
    def machine_state(self):
        return self._machine_state

    @machine_state.setter
    def machine_state(self, arg):
        self._machine_state = arg
        self._notify()


class SocketClient(socket.socket):

    def __init__(self, host: str = "localhost", port: int = 8888) -> None:
        super().__init__()
        self._ADDRESS = host, port

    def call(self, message: Union[None, str] = None):
        with self as sock:
            sock.connect(self._ADDRESS)
            sock.send(bytes(message, encoding='utf-8'))
            return str(sock.recv(1024), encoding="utf-8")


class SocketMachine(Machine):

    def __init__(self, client: SocketClient):
        super().__init__()
        self._client = client
        self._collections.add(self._client)


class HttpMachine(Machine):

    def __init__(self):
        super().__init__()


class Observer(metaclass=abc.ABCMeta):
    """
    Observer object
    """

    def __init__(self):
        self._machine = None
        self._action_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class Action(Observer):
    """
    Action object
    """

    def update(self, arg):
        self._action_state = arg
