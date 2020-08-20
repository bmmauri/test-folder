import unittest
import unittest.mock as mock

from tf.core.engine import SocketMachine, HttpMachine, Action, SocketClient


class EngineTestCase(unittest.TestCase):

    @unittest.skip
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
