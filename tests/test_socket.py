import logging
import unittest

from tf.core.engine import SocketMachine
from tf.mock.client import MockTCPClient
from tf.mock.server import MockTCPServer


class SocketTestCase(unittest.TestCase):

    def test__socket_machine_call(self):
        """TestCase: MockTCPClient call."""
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        machine.server.fork_until(interval=3, detach=True)
        response = machine._client.call(**{
            "message": "hello python"
        })
        logging.info(response)
        self.assertIsNotNone(response, msg="Message received should not be empty")


if __name__ == '__main__':
    unittest.main()
