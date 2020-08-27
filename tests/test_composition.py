import logging
import pickle
import time
import unittest

from tf import utils
from tf.core.engine import SocketMachine, MachineState
from tf.mixture import TestFolderCompose, TestFolderExecution
from tf.mock.client import MockTCPClient
from tf.mock.command import Start, Pause, Abort
from tf.mock.server import MockTCPServer, MockSocketStateHandler

logger = logging.getLogger()
handler = logging.FileHandler(filename=f"{logger.name}.log", mode="w")
handler.setFormatter(utils.Formatter())
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class ComposeTestCase(unittest.TestCase):

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

    def test__compose(self):
        """TestCase: MockTCPClient call."""
        tf_compose = TestFolderCompose()
        tf_compose.instance.setup(
            machine=SocketMachine(client=MockTCPClient(), server=MockTCPServer()),
            execution=TestFolderExecution(context={"message": "Hi! I am TestAutomation."})
        )
        self.assertTrue(
            tf_compose.instance.machine is not None and tf_compose.instance.execution is not None,
            "Machine and Execution object must declared before composing"
        )

    def test__execution_simple(self):
        """TestCase: Simple execution of a test"""
        tf_compose = TestFolderCompose()
        tf_compose.instance.setup(
            machine=SocketMachine(client=MockTCPClient(), server=MockTCPServer()),
            execution=TestFolderExecution(context={"message": "Hi! I am TestAutomation."})
        )
        tf_compose.instance.machine.server.fork_until(detach=True)
        tf_compose.instance.execution.execute()
        tf_compose.instance.machine.server._wait_until_close()
        self.assertIsNotNone(tf_compose.instance.execution.extract(), "Extraction failure")

    def test__execution_start(self):
        """TestCase: Simple execution of a test: START"""
        tf_compose = TestFolderCompose()
        tf_compose.instance.setup(
            machine=SocketMachine(client=MockTCPClient(), server=MockTCPServer(handler=MockSocketStateHandler)),
            execution=TestFolderExecution(
                context={
                    "message": pickle.dumps(Start())
                }
            )
        )
        tf_compose.instance.machine.server.fork_until(detach=True)
        tf_compose.instance.execution.execute()
        tf_compose.instance.machine.server._wait_until_close()
        self.assertIn("Transition", tf_compose.instance.execution.extract(), "Extraction failure")

    def test__execution_pause(self):
        """TestCase: Simple execution of a test: PAUSE"""
        tf_compose = TestFolderCompose()
        tf_compose.instance.setup(
            machine=SocketMachine(client=MockTCPClient(), server=MockTCPServer(handler=MockSocketStateHandler)),
            execution=TestFolderExecution(
                context={
                    "message": pickle.dumps(Pause())
                }
            )
        )
        tf_compose.instance.machine.server.fork_until(detach=True)
        tf_compose.instance.execution.execute()
        tf_compose.instance.machine.server._wait_until_close()
        self.assertEqual(tf_compose.instance.machine.machine_state, MachineState.FINISH, "Wrong machine state")

    def test__execution_pause_then_abort(self):
        """TestCase: Simple execution of a test: PAUSE then ABORT"""
        tf_compose = TestFolderCompose()
        tf_compose.instance.setup(
            machine=SocketMachine(client=MockTCPClient(), server=MockTCPServer(handler=MockSocketStateHandler)),
            execution=TestFolderExecution(
                context={
                    "message": pickle.dumps(Pause())
                }
            )
        )
        tf_compose.instance.machine.server.fork_until(detach=True)
        tf_compose.instance.execution.execute()
        time.sleep(8)
        MockTCPClient().call(**{
            "message": pickle.dumps(Abort())
        })
        tf_compose.instance.machine.server._wait_until_close()
        self.assertEqual(tf_compose.instance.machine.machine_state, MachineState.FINISH, "Wrong machine state")


if __name__ == '__main__':
    unittest.main()
