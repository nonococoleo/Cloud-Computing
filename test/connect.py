import sys
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from MyOwnPeer2PeerNode import MyOwnPeer2PeerNode

# This is the local node instance we already initialize in server.py.
node_1 = MyOwnPeer2PeerNode("127.0.0.1", 10001)

# connect to outbond nodes
node_1.connect_with_node('35.172.132.81', 8001)
node_1.connect_with_node('52.204.229.153', 8002)

#send messages to all connected nodes

#try sending string
node_1.send_to_nodes("message: Hi there! I am Lin")

#try sending image
with open("IMG_4632.jpg", "rb") as image_file:
    data = base64.b64encode(image_file.read())
node_1.send_to_nodes(data.decode())

#try sending json
node_1.send_to_nodes({
               "constant": False,
               "inputs": [
                   {
                       "name": "numberSelected",
                       "type": "uint256"
                   }
               ],
               "name": "bet",
               "outputs": [],
               "payable": True,
               "stateMutability": "payable",
               "type": "function"
           })