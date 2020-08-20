import unittest

from tf.core.engine import SocketMachine, SocketClient


class EngineTestCase(unittest.TestCase):

    def test__socket_machine_call(self):
        """
        Test socket call.
        """
        machine = SocketMachine(client=SocketClient(port=8888))
        response = machine._client.call(**{
            "message": "hello python"
        })
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
