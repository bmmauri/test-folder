import logging
import pickle
import unittest

from tf import utils
from tf.core.engine import RoboticMachine
from tf.mixture import TestFolderCompose, TestFolderExecution
from tf.mock.client import MockTCPClient
from tf.mock.command import Start

logger = logging.getLogger()
handler = logging.FileHandler(filename=f"{logger.name}.log", mode="w")
handler.setFormatter(utils.Formatter())
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class RoboticMachineTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logger.info(f"{'##' * 20}\n START TESTSUITE: {cls.__name__}\n{'##' * 20}")

    def setUp(self) -> None:
        super().setUp()
        logger.info(f"RUNNING: {self.__class__.__name__}: '{self._testMethodName}' method")

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        logger.info(f"{'##' * 20}\n END TESTSUITE: {cls.__name__}\n{'##' * 20}")

    def test__robotic_server_machine(self):
        """TestCase: RoboticServer call."""
        tf_compose = TestFolderCompose()
        tf_compose.instance.setup(
            machine=RoboticMachine(client=MockTCPClient()),
            execution=TestFolderExecution(
                context={
                    "message": pickle.dumps(Start())
                }
            )
        )
        self.assertTrue(False, msg="Message received should not be empty")


if __name__ == '__main__':
    unittest.main()
