import unittest

from tf.core.engine import SocketMachine
from tf.mock.client import MockTCPClient
from tf.mock.server import MockTCPServer


class EngineTestCase(unittest.TestCase):

    def test__socket_machine_call(self):
        """TestCase: MockTCPClient call."""
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        response = machine._client.call(**{
            "message": "hello python"
        })
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
