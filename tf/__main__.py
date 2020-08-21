import argparse

from tf.mock.server import MockTCPServer


def mock(args):
    if args.host and args.port:
        mock_server = MockTCPServer(
            host=args.host, port=args.port
        )
        mock_server.fork_until(interval=args.open_time, detach=bool(args.detach))


parser = argparse.ArgumentParser(description='Easy Mock socket server')
subparsers = parser.add_subparsers()
mock_parser = subparsers.add_parser('mock', help='Mock client|server')
mock_parser.add_argument('--host', help='Socket hostname', required=True)
mock_parser.add_argument('--port', help='Socket port', type=int, required=True)
mock_parser.add_argument('--open-time', help="Listening open time of server", type=int, default=5)
mock_parser.add_argument('--detach', help="Enable detach mode", type=bool, default=False)
mock_parser.set_defaults(func=mock)
arguments = parser.parse_args()
arguments.func(arguments)
