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

    node = MyOwnPeer2PeerNode(host, port, modules)

    node.start()
    node.connect_with_node("127.0.0.1", 10000)

    # node.send_to_nodes({"type": "test"})
    # node.stop()
