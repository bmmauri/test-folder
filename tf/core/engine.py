"""
Engine module
    - Machine object
"""
import abc
import enum


class MachineState(enum.Enum):
    ABORT = 0
    START = 1
    RUN = 2
    PAUSE = 3
    BLOCK = 4
    FINISH = 5


class Machine:

    def __init__(self):
        self._actions = set()
        self._machine_state = None

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


class SocketMachine(Machine):

    def __init__(self):
        super().__init__()


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
