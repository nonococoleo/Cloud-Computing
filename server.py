from ServerNode import MyOwnPeer2PeerNode

import argparse

parser = argparse.ArgumentParser(description='CHANGE THIS')

parser.add_argument('-d', '--dest', default='127.0.0.1', type=str,
                    help='CHANGE THIS')

parser.add_argument('-p', '--port', default=10000, type=int,
                    help='CHANGE THIS')

parser.add_argument('-m', '--modules', default="", type=str,
                    help='CHANGE THIS')

args = parser.parse_args()

if __name__ == '__main__':
    host = args.dest
    port = args.port

    modules = filter(len, [s.strip() for s in args.modules.split(',')])

    # Open local port, argument "True" meaning initializing server.
    node_1 = MyOwnPeer2PeerNode(host, port, modules)

    # node started
    node_1.start()
    # node_1.connect_with_node("127.0.0.1", 10002)

    # node_1.send_to_nodes({"type": "test"})
    # node_1.stop()
