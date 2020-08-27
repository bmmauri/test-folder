import logging
import unittest

from tf import Action
from tf import utils
from tf.core.engine import HttpMachine, SocketMachine, Machine, MachineState
from tf.mock.client import MockTCPClient
from tf.mock.server import MockTCPServer

logger = logging.getLogger()
handler = logging.FileHandler(filename=f"{logger.name}.log", mode="w")
handler.setFormatter(utils.Formatter())
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class EngineTestCase(unittest.TestCase):

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

    def test__machine_multiple_actions(self):
        """
        Test the number of attachments into the machine.
        """
        machine = Machine()
        attachments = [machine.attach(Action()) for i in range(5)]
        self.assertEqual(len(machine._actions), len(attachments))

    def test__socket_machine_multiple_actions(self):
        """
        Test the number of attachments into the socket machine.
        """
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        attachments = [machine.attach(Action()) for i in range(5)]
        self.assertEqual(len(machine._actions), len(attachments) + len(machine._collections))

    def test__socket_machine_state_after_machine_started(self):
        """
        Test machine state after start server.
            - MachineState.START
        """
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        self.assertIs(
            machine.machine_state, MachineState.START,
            f'Expected state {MachineState.START.name} got {machine.machine_state.name}'
        )

    def test__socket_machine_state_after_server_run(self):
        """
        Test machine state after start server.
            - MachineState.RUN
        """
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        machine._server.fork_until(interval=2, detach=True)
        self.assertIs(
            machine.machine_state, MachineState.RUN,
            f'Expected state {MachineState.RUN.name} got {machine.machine_state.name}'
        )

    def test__socket_machine_state_after_server_finished(self):
        """
        Test machine state after finish server.
            - MachineState.FINISH
        """
        machine = SocketMachine(
            client=MockTCPClient(port=8888),
            server=MockTCPServer(port=8888)
        )
        machine._server.fork_until(interval=2, detach=False)
        self.assertIs(
            machine.machine_state, MachineState.FINISH,
            f'Expected state {MachineState.FINISH.name} got {machine.machine_state.name}'
        )

    def test__http_machine_multiple_actions(self):
        """
        Test the number of attachments into the http machine.
        """
        machine = HttpMachine()
        attachments = [machine.attach(Action()) for i in range(5)]
        self.assertEqual(len(machine._actions), len(attachments))


class EngineMachineStateTestCase(unittest.TestCase):

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

    def test__machine_abort(self):
        """
        Test the state of the machine: MachineState.ABORT.
        """
        machine = Machine()
        machine.abort()
        self.assertEqual(machine._machine_state, MachineState.ABORT)

    def test__machine_start(self):
        """
        Test the state of the machine: MachineState.START.
        """
        machine = Machine()
        machine.start()
        self.assertEqual(machine._machine_state, MachineState.START)

    def test__machine_run(self):
        """
        Test the state of the machine: MachineState.RUN.
        """
        machine = Machine()
        machine.run()
        self.assertEqual(machine._machine_state, MachineState.RUN)

    def test__machine_pause(self):
        """
        Test the state of the machine: MachineState.PAUSE.
        """
        machine = Machine()
        machine.pause()
        self.assertEqual(machine._machine_state, MachineState.PAUSE)

    def test__machine_block(self):
        """
        Test the state of the machine: MachineState.BLOCK.
        """
        machine = Machine()
        machine.block()
        self.assertEqual(machine._machine_state, MachineState.BLOCK)

    def test__machine_finish(self):
        """
        Test the state of the machine: MachineState.FINISH.
        """
        machine = Machine()
        machine.finish()
        self.assertEqual(machine._machine_state, MachineState.FINISH)

    def test__machine_init(self):
        """
        Test the state of the machine: MachineState.INIT.
        """
        machine = Machine()
        machine.init()
        self.assertEqual(machine._machine_state, MachineState.INIT)

    def test__machine_complete(self):
        """
        Test the state of the machine: MachineState.FINISH.
        """
        machine = Machine()
        machine.complete()
        self.assertEqual(machine._machine_state, MachineState.COMPLETE)


if __name__ == '__main__':
    unittest.main()
