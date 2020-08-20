import random
import unittest

from tf.core.engine import HttpMachine, SocketMachine, Machine, Action, MachineState


class EngineTestCase(unittest.TestCase):
    def test__machine_multiple_actions(self):
        """
        Test the number of attachments into the machine.
        """
        machine = Machine()
        attachments = [machine.attach(Action()) for i in range(random.randint(2, 19))]
        self.assertEqual(len(machine._actions), len(attachments))

    def test__socket_machine_multiple_actions(self):
        """
        Test the number of attachments into the socket machine.
        """
        machine = SocketMachine()
        attachments = [machine.attach(Action()) for i in range(random.randint(2, 19))]
        self.assertEqual(len(machine._actions), len(attachments))

    def test__http_machine_multiple_actions(self):
        """
        Test the number of attachments into the http machine.
        """
        machine = HttpMachine()
        attachments = [machine.attach(Action()) for i in range(random.randint(2, 19))]
        self.assertEqual(len(machine._actions), len(attachments))


class EngineMachineStateTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
