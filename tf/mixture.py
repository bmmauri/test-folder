"""
'mixture' module
    - Mixture generic object
    - Execution generic implementation of an automated scheduled request
    - TestFolder happy class
"""

import abc

from tf import Action
from tf.core.engine import SocketMachine


class Execution(Action, metaclass=abc.ABCMeta):
    """
    Generic Execution class to define the behaviour of a TestExecution.
    """

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def extract(self):
        pass


class TestFolderExecution(Execution):
    """
    Happy Execution object
    """

    result = None

    def __init__(self, context: dict = None) -> None:
        """
        Concrete expected execution prepared for automation.

        :param context: desired content of the executor
        """
        super().__init__()
        self._context = context

    @property
    def context(self):
        return self._context

    def execute(self):
        machine: SocketMachine = self.get_machine()
        self.result = machine.client.call(**self._context)

    def extract(self):
        return self.result


class TestFolder:
    """
    Happy composition object that contain a machine and an execution
    """
    machine: SocketMachine = None
    execution: TestFolderExecution = None

    def setup(self, machine, execution):
        """
        Setup with machine and execution, execution must attach to machine.

        :param machine: SocketMachine object
        :param execution: TestFolderExecution object
        :return:
        """
        self.machine = machine
        self.execution = execution
        self.machine.attach(self.execution)


class Mixture(metaclass=abc.ABCMeta):
    """
    Mixture generic object, should be implemented by a concrete class.
    """

    def __init__(self) -> None:
        """Generic instance of a mixture object"""
        self.instance = self._get_instance()

    @abc.abstractmethod
    def _get_instance(self):
        pass


class TestFolderCompose(Mixture):
    """
    TestFolder mixture object
    """

    def _get_instance(self):
        return TestFolder()
