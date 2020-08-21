"""
'test-folder' a test automation framework.
"""
import abc
from typing import Union

import tf.core.engine as engine


class Observer(metaclass=abc.ABCMeta):
    """
    Observer object
    """

    def __init__(self):
        self._machine: Union[engine.Machine, None] = None
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
