# Cloud-Computing

#### example
1. Build a P2P network
```bash
# start a server by default settings
python3 server.py
# start a server with FaceRecognition Module 
python3 server.py -d localhost -p 10001 -m FaceRecognition
```

2. Connect user node to any of node in the P2P network and send request
```bash
python3 user.py -p 10002
```
