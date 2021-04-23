import sys
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from MyOwnPeer2PeerNode import MyOwnPeer2PeerNode

node_1 = MyOwnPeer2PeerNode("192.168.50.149", 10001)

node_1.connect_with_node('35.172.132.81', 8001)
node_1.connect_with_node('52.204.229.153', 8002)

node_1.send_to_nodes("message: Hi there! I am Lin")