import sys
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from MyOwnPeer2PeerNode import MyOwnPeer2PeerNode

# Open local port, argument "True" meaning initializing server.
node_1 = MyOwnPeer2PeerNode("127.0.0.1", 10001, True)

# node started
node_1.start()
