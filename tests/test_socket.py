import logging
import unittest

from tf import utils
from tf.core.engine import SocketMachine
from tf.mock.client import MockTCPClient
from tf.mock.server import MockTCPServer

logger = logging.getLogger()
handler = logging.FileHandler(filename=f"{logger.name}.log", mode="w")
handler.setFormatter(utils.Formatter())
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class SocketTestCase(unittest.TestCase):

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

    def test__socket_machine_call(self):
        """TestCase: MockTCPClient call."""
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        machine.server.fork_until(interval=3, detach=True)
        response = machine._client.call(**{
            "uid": None,
            "headers": {
                "author": "test-folder-automation",
                "content": None
            },
            "message": "hello python"
        })
        logging.info(response)
        machine.server._wait_until_close()
        self.assertIsNotNone(response, msg="Message received should not be empty")


if __name__ == '__main__':
    unittest.main()
