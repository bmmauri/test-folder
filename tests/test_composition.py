import pickle
import unittest

from tf.core.engine import SocketMachine
from tf.mixture import TestFolderCompose, TestFolderExecution
from tf.mock.client import MockTCPClient
from tf.mock.command import Start
from tf.mock.server import MockTCPServer, MockSocketStateHandler


class ComposeTestCase(unittest.TestCase):

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
        self.assertEqual("START", tf_compose.instance.execution.extract(), "Extraction failure")


if __name__ == '__main__':
    unittest.main()
