import time
import base64

from utilities import *
from ServerNode import MyOwnPeer2PeerNode

import argparse

parser = argparse.ArgumentParser(description='CHANGE THIS')

parser.add_argument('-d', '--dest', default='127.0.0.1', type=str,
                    help='CHANGE THIS')

parser.add_argument('-p', '--port', default=10000, type=int,
                    help='CHANGE THIS')

args = parser.parse_args()

if __name__ == '__main__':
    host = args.dest
    port = args.port

    # Open local port, argument "True" meaning initializing server.
    node_1 = MyOwnPeer2PeerNode(host, port, [])

    # node started
    node_1.start()
    connected_node = node_1.connect_with_node("127.0.0.1", 10001)

    file = "ident.JPG"
    with open(file, 'rb') as image:
        img = image.read()

    base64_bytes = base64.b64encode(img)
    base64_string = base64_bytes.decode('utf-8')

    node_1.send_to_node(connected_node,
                        {"type": "FaceRecognition", "content": {"image_data": base64_string}, "origin": node_1.id,
                         "to": connected_node.id, "id": get_md5(base64_string)})

    time.sleep(10)
    node_1.stop()