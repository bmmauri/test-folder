"""
'test-folder' a test automation framework.
"""
import abc
from typing import Union

import tf.core.engine as engine


class Observer(metaclass=abc.ABCMeta):
    """Observer object."""

    def __init__(self) -> None:
        """Metaclass object that expose the machine and the action state of the concrete object."""
        self._machine: Union[engine.Machine, None] = None
        self._action_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass

    def get_machine(self):
        return self._machine


class Action(Observer):
    """Action concrete observer object."""

    def update(self, arg):
        self._action_state = arg
