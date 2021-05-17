# Cloud-Computing

#### example
1. Build a P2P network
```bash
# start a server by default settings
python3 server.py
# start a server with FaceRecognition Module 
python3 server.py -d localhost -p 10001 -m FaceRecognition,ConnectCamera
```

2. Start a worker node waiting for images from iot node
```bash
python3 worker.py -p 20000
```

3. Start a iot node sending images on a regular interval 10 seconds
```bash
python3 camera.py --interval 10
```

4. Connect user node to any of node in the P2P network and send request
```bash
python3 user.py -p 10002
```

#### note
* message format in the p2p network
```json
{"type": "string","content": "dict","from": "string", "to": "string","origin": "string"}
```

#### installation guide
1.set up your own blockchain  

- Since we cannot include the blockchain service in the github, you can first setup the blockchain service after clone the code  
- Using the VS code to setup the blockchain
- https://docs.microsoft.com/en-us/azure/blockchain/service/connect-vscode
- Generate a basic blockchain project and replace the Helloblockchain.sol with the file from our project  
- Right click the .sol file and build the contract then right click to deploy the contract   
- Replace network field in ConnenctBlockChain.py with the value in truffle-config.js start with "abs_xxxxxxxx"
- Then you could test the blockchain module by running the main method in ConnenctBlockChain.py   