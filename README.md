# Cloud-Computing
#### installation guide
1. set up your own blockchain  

- Since we cannot include the blockchain service in the github, you can first setup the blockchain service after clone the code  
- Using the VS code to setup the blockchain
- https://docs.microsoft.com/en-us/azure/blockchain/service/connect-vscode
- Generate a basic blockchain project and replace the Helloblockchain.sol with the file from our project  
- Right click the .sol file and build the contract then right click to deploy the contract   
- Replace network field in ConnenctBlockChain.py with the value in truffle-config.js start with "abs_xxxxxxxx"
- Then you could test the blockchain module by running the main method in ConnenctBlockChain.py   

2. create a s3 bucket, follow the example below:
https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html

3. create a IOT device, follow the example below:
https://docs.aws.amazon.com/iot/latest/developerguide/using-laptop-as-device.html

4. create AWS IAM user with privilege to S3 and Rekognition service, follow the example below
https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_billing.html

#### Modify settings
1. Config AWS account access keys, create ./config.py and insert the example code with your keys. Note the account must have an S3 storage availble and AWS Rekognition service intialized.
```python
aws = {'access_key_id': 'your key', 'secret_access_key': 'your key'}
```
2. Here we want to configure buckets name for face recognition. In camera.py, change the bucket name to the S3 storage created on aws account, the location of the code is on line 33. Also, apply same rule in FaceRecognition.py at line 37.
```python
parser.add_argument('--bucket', type=str, default='your s3 name', help="Amazon S3 bucket to store images")
```
3. Now config AWS IOT service. Detailed AWS configuration refer to this tutorial (https://docs.aws.amazon.com/iot/latest/developerguide/using-laptop-as-device.html). After the IOT service started, we should be able to get three keys and an endpoint.  They are certification keys, aws private keys, iam root keys and iot service endpoint. Create a file somewhere in workspace and replace the 'change me' line in both worker.py and camera.py with relative address of keys.
```python
parser.add_argument('--endpoint', default='CHANGE THIS',
                    help="Your AWS IoT custom endpoint, not including a port. ")
parser.add_argument('--cert', default='CHANGE THIS',
                    help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', default='CHANGE THIS',
                    help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', default='CHANGE THIS',
                    help="File path to root certificate authority, in PEM format. ")
//change as
parser.add_argument('--endpoint', default='aaaaa.iot.us-west-1.amazonaws.com',
                    help="Your AWS IoT custom endpoint, not including a port. ")
parser.add_argument('--cert', default='keys/my_iot_certification.pem.crt',
                    help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', default='keys/my_aws_private_key',
                    help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', default='keys/my_aws_iam_root_key',
                    help="File path to root certificate authority, in PEM format. ")
```

4. Now all the prerequisite is settled. However, to make the project fully runnable, we also need a blockchain module, we put the blockchain module at the bottom of this doc, Since it is relativly complicate. 

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
