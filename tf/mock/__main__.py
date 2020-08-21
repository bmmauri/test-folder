import argparse

from tf.mock.server import MockTCPServer

parser = argparse.ArgumentParser(description='Easy Mock socket server')
parser.add_argument('--host', help='Socket hostname', required=True)
parser.add_argument('--port', help='Socket port', type=int, required=True)
parser.add_argument('--open-time', help="Listening open time of server", type=int, default=5)
parser.add_argument('--detach', help="Enable detach mode", type=bool, default=False)

args = parser.parse_args()
if args.host and args.port:
    mock_server = MockTCPServer(
        host=args.host, port=args.port
    )
    mock_server.fork_until(interval=args.open_time, detach=bool(args.detach))
