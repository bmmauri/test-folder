import json
import logging
import msgpack
import os
import pickle
import unittest

from tf import utils
from tf.core.engine import RoboticMachine
from tf.mixture import TestFolderCompose, TestFolderExecution
from tf.mock.client import MockTCPClient
from tf.mock.command import Run

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

    def test__robotic_server_microprocessor(self):
        """TestCase: RoboticServer microprocessor ex"""
        tf_compose = TestFolderCompose()
        robot_machine = RoboticMachine(client=MockTCPClient())
        robot_machine.microprocessor.update({
            "ip": "192.168.4.2", "port": 80, "uri": "/"
        })
        tf_compose.instance.setup(
            machine=robot_machine,
            execution=TestFolderExecution(
                context={
                    "message": pickle.dumps(Run(
                        command=json.dumps(
                            {"s1": 60, "s4": 20}
                        )
                    ))
                }
            )
        )
        micro = tf_compose.instance.machine.microprocessor
        self.assertIsNotNone(micro, msg="Message received should not be empty")

    def test__robotic_server_machine(self):
        """TestCase: RoboticServer call."""
        tf_compose = TestFolderCompose()
        robot_machine = RoboticMachine(client=MockTCPClient())
        robot_machine.microprocessor.update({
            "ip": "192.168.4.2", "port": 80, "uri": "/servo/"
        })
        tf_compose.instance.setup(
            machine=robot_machine,
            execution=TestFolderExecution(
                context={
                    "message": pickle.dumps(Run(
                        command=json.dumps(
                            {"s0": 10}
                        )
                    ))
                }
            )
        )
        tf_compose.instance.machine.server.fork_until(interval=5, detach=True)
        tf_compose.instance.execution.execute()
        response = tf_compose.instance.execution.extract()
        tf_compose.instance.machine.server._wait_until_close()
        self.assertIsNotNone(response, msg="Message received should not be empty")


if __name__ == '__main__':
    unittest.main()
