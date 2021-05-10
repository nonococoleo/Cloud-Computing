import signal
from datetime import datetime

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

    node = MyOwnPeer2PeerNode(host, port, [])

    node.start()
    node.connect_with_node("127.0.0.1", 10000)

    # IOT request
    data = {"type": "ConnectCamera", "content": {"interval": 60}, "origin": node.id}

    node.send_to_node_with_resource(data)

    # ML request
    file = "files/images/1.jpg"
    bucket = "ccsp21proj2"
    obj_name = upload_image("user", file, bucket)

    node.send_to_node_with_resource(
        {"type": "FaceRecognition", "content": {"image_file": (bucket, obj_name)}, "origin": node.id})

    # BLOCKCHAIN request
    data = {"type": "ConnectBlockChain",
            "content": {"type": "getData", "data": {"date": datetime.today().strftime('%Y-%m-%d'), "field": "visitor"}},
            "origin": node.id}

    node.send_to_node_with_resource(data)

    signal_handler = lambda sig, frame: node.stop()

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
