import argparse

from tf.mock.server import MockTCPServer, MockSocketHandler

parser = argparse.ArgumentParser(description='Easy Mock socket server')
parser.add_argument('--host', help='Socket hostname', required=True)
parser.add_argument('--port', help='Socket port', type=int, required=True)
parser.add_argument('--open-time', help="Listening open time of server", type=int, default=5)

args = parser.parse_args()

if args.host and args.port:
    mock_server = MockTCPServer(
        host=args.host, port=args.port,
        handler=MockSocketHandler
    )
    mock_server.fork_until(_method=mock_server.run, interval=args.open_time)
