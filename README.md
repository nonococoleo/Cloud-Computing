# Cloud-Computing

### Update on Apr.28:

Now the framework support tranfering images. Note that if the image file is too huge the process may fail.



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

### 3. Image Tranfering

Require installation of PIL package on all peers by running:

`pip install image`

Then on the sending peer, we need to first convert img (for example .jpg format) into base64 bytes

```python
import base64
from PIL import Image
from io import BytesIO

with open("img1.jpg", "rb") as image_file:
    data = base64.b64encode(image_file.read())
```

Then convert the bytes to string to send data

```python
node_1.send_to_nodes(data.decode())
```

On the receiving side, we need to decode the data received by trying if the data can be converted back to a image, if not , try if it can be decoded into json file or a str. This requires modify in `parse_packet` function in `nodeconnection.py` as follows:

```python
def parse_packet(self, packet):
    """Parse the packet and determines wheter it has been send in str, json or byte format. It returns
           the according data."""
    try:
        # try to decode with utf-8 
        packet_decoded = packet.decode('utf-8')
        try:
            # try if can be converted into an image
            im = Image.open(BytesIO(base64.b64decode(packet_decoded)))
            curTime = datetime.datetime.now().strftime("%I:%M%p%d%B%Y")
            #this is the file path to store image received, change it
            #according to your own environment
            imageFile = '/home/ubuntu/python-p2p-network/images/Img'+curTime+'.jpg'
            im.save(imageFile)
            return imageFile + " received"
        except:
            # if cannnot be converted into an image, try json
            try:
                return json.loads(packet_decoded)

            except json.decoder.JSONDecodeError:
                # if still not, then the data received is just a string
                return packet_decoded

    except UnicodeDecodeError:
        # data received cannot be deceoded
        return packet
```

Note that we name the image file with receiving time and save it to path `imageFile`, which should be modified in your environment.