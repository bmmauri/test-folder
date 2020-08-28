echo "---- RUNNING TEST ------"
python -m pytest --disable-pytest-warnings --html=reports/test_engine_machine_state.html tests/test_engine.py::EngineMachineStateTestCase --cache-clear
python -m pytest --disable-pytest-warnings --html=reports/test_engine.html tests/test_engine.py::EngineTestCase --cache-clear
sleep 5
python -m pytest --disable-pytest-warnings --html=reports/test_composition.html tests/test_composition.py::ComposeTestCase --cache-clear
sleep 10
python -m pytest --disable-pytest-warnings --html=reports/test_socket.html tests/test_socket.py::SocketTestCase --cache-clear
sleep 5
echo "---- COMPLETED TEST ------"
