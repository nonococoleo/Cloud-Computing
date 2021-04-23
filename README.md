# Cloud-Computing

### 1. P2P framework Installation

The requirement is python >= 3.6. We could use conda to manage the environment. Run the following:

```bash
conda create --name p2p python=3.6
conda activate p2p
pip install p2pnetwork
```

### 2. Usage

We mainly focus on the folder **test**.

**server.py** starts a local TCP port. To start a server:

`python server.py`

**connect.py** connects outbound nodes and send messages. To run the code:

`python connect.py`

**MyOwnPeer2PeerNode.py** can be used to extend the nodes functionality.

