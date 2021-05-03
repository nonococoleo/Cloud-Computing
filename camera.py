import boto3
import botocore
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from uuid import uuid4

import sys
import threading
import json
import time

from utilities import *

import argparse

parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
parser.add_argument('--endpoint', default='a2xwqc692xy96k-ats.iot.us-east-2.amazonaws.com',
                    help="Your AWS IoT custom endpoint, not including a port. ")
parser.add_argument('--cert', default='certs/20cd5b421f-certificate.pem.crt',
                    help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', default='certs/20cd5b421f-private.pem.key',
                    help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', default='certs/AmazonRootCA1.pem',
                    help="File path to root certificate authority, in PEM format. ")
parser.add_argument('--client-id', default=str(uuid4()), help="Client ID for MQTT connection.")
parser.add_argument('--use-websocket', default=False, action='store_true',
                    help="To use a websocket instead of raw mqtt. If you " +
                         "specify this option you must specify a region for signing, you can also enable proxy mode.")
parser.add_argument('--signing-region', default='us-east-2', help="If you specify --use-web-socket, this " +
                                                                  "is the region that will be used for computing the Sigv4 signature")
parser.add_argument('--proxy-host', help="Hostname for proxy to connect to. Note: if you use this feature, " +
                                         "you will likely need to set --root-ca to the ca for your proxy.")
parser.add_argument('--proxy-port', type=int, default=8080, help="Port for proxy to connect to.")

parser.add_argument('--bucket', type=str, default='ccsp21spring', help="Amazon S3 bucket to store images")

parser.add_argument('--interval', type=int, default=10, help="Amazon S3 bucket to store images")

# Using globals to simplify sample code
args = parser.parse_args()


class Camera:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

        self.shutdown_flag = threading.Event()
        self.id = args.endpoint.split('-')[0]
        self.interval = args.interval

        # Spin up resources
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

        if args.use_websocket == True:
            proxy_options = None
            if (args.proxy_host):
                proxy_options = http.HttpProxyOptions(host_name=args.proxy_host, port=args.proxy_port)

            credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)
            self.mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
                endpoint=args.endpoint,
                client_bootstrap=client_bootstrap,
                region=args.signing_region,
                credentials_provider=credentials_provider,
                websocket_proxy_options=proxy_options,
                ca_filepath=args.root_ca,
                on_connection_interrupted=self.on_connection_interrupted,
                on_connection_resumed=self.on_connection_resumed,
                client_id=args.client_id,
                clean_session=False,
                keep_alive_secs=60)

        else:
            self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=args.endpoint,
                cert_filepath=args.cert,
                pri_key_filepath=args.key,
                client_bootstrap=client_bootstrap,
                ca_filepath=args.root_ca,
                on_connection_interrupted=self.on_connection_interrupted,
                on_connection_resumed=self.on_connection_resumed,
                client_id=args.client_id,
                clean_session=False,
                keep_alive_secs=60)

        self.logger.debug("Connecting to {} with client ID '{}'...".format(
            args.endpoint, args.client_id))

        connect_future = self.mqtt_connection.connect()

        # Future.result() waits until a result is available
        connect_future.result()
        self.logger.info(f"Connected with {args.endpoint}")

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(self, connection, error, **kwargs):
        self.logger.error("Connection interrupted. error: {}".format(error))

    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        self.logger.info("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            self.logger.info("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self.on_resubscribe_complete)

    def on_resubscribe_complete(self, resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        self.logger.info("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))

    # Callback when the subscribed topic receives a message
    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs):
        payload_decoded = payload.decode('utf-8')
        data = json.loads(payload_decoded)
        self.logger.debug("Received message from topic '{}': {}".format(topic, data))
        if data["type"] == "manage":
            self.interval = data["content"]["interval"]
            self.logger.info(f"change interval to {self.interval}")
        else:
            self.logger.error(f"action {data['type']} not supported.")

    def subscribe(self, topic):
        # Subscribe
        self.logger.info("Subscribing to topic '{}'...".format(topic))
        subscribe_future, packet_id = self.mqtt_connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_message_received)

        subscribe_result = subscribe_future.result()
        self.logger.info("Subscribed with {}".format(str(subscribe_result['qos'])))

    def publish(self, topic, message):
        self.logger.info("Publishing message to topic '{}': {}".format(topic, message))
        self.mqtt_connection.publish(
            topic=topic,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE)

    def run(self):
        count = 1
        while not self.shutdown_flag.is_set():
            self.send_image(f'files/images/{count}.jpg')
            count += 1
            time.sleep(self.interval)

        self.shutdown_flag.wait()

        # Disconnect
        self.logger.debug("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        self.logger.info("Disconnected!")

    def shutdown(self):
        self.logger.info("shutdown...")
        self.shutdown_flag.set()

    def send_image(self, file):
        s3 = boto3.client('s3',
                          aws_access_key_id='AKIASZTGMVDZGAN5L3B2',
                          aws_secret_access_key='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',
                          )
        bucket = args.bucket
        obj_name = f'{self.id}-{time.time()}.jpg'
        try:
            s3.upload_file(file, bucket, obj_name)
        except botocore.exceptions.ClientError as e:
            self.logger.error(str(e))

        data = {"type": "image", "content": {"image": (bucket, obj_name)}, "origin": self.id,
                "id": get_md5(file)}
        c.publish("camera/image", json.dumps(data))
        self.logger.info("image uploaded.")


if __name__ == '__main__':
    c = Camera()
    c.subscribe("camera/manage")
    main = threading.Thread(target=c.run)
    main.start()

    time.sleep(30)
    c.shutdown()
    main.join()
