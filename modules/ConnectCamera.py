import time
import json

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from uuid import uuid4

endpoint = 'CHANGE THIS'
cert = 'CHANGE THIS'
key = 'CHANGE THIS'
root_ca = 'CHANGE THIS'
client_id = str(uuid4())


def send_message(topic, message):
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=cert,
        pri_key_filepath=key,
        client_bootstrap=client_bootstrap,
        ca_filepath=root_ca,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=60)

    connect_future = mqtt_connection.connect()
    connect_future.result()

    mqtt_connection.publish(
        topic=topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE)

    time.sleep(1)


def main(settings):
    data = {"type": "manage", "data": settings}
    send_message("camera/manage", json.dumps(data))
    return True


if __name__ == '__main__':
    res = main({"type": "manage", "data": {"interval": 50}})
    print(res)
