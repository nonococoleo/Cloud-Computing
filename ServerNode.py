from p2pnetwork.node import Node

import importlib
import random
import socket
import time
import os

from utilities import *


class MyOwnPeer2PeerNode(Node):
    def __init__(self, host, port, modules):
        self.logger = get_logger(self.__class__.__name__)

        super(MyOwnPeer2PeerNode, self).__init__(host, port)
        self.id = self.id[:8]

        self.modules = {}
        for i in modules:
            self.modules[i] = importlib.import_module(f"modules.{i}")
        self.resources = list(self.modules.keys())
        self.neighbors = {}

        self.logger.info(f"MyPeer2PeerNode: {self.id} Started")

    def init_server(self):
        self.logger.debug("Initialisation of the Node on port: " + str(self.port) + " on node (" + self.id + ")")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10)
        self.sock.listen(1)

    def run(self):
        while not self.terminate_flag.is_set():
            try:
                self.logger.debug("Node: Wait for incoming connection")
                connection, client_address = self.sock.accept()

                connected_node_id = connection.recv(4096).decode('utf-8')
                connection.send(self.id.encode('utf-8'))

                thread_client = self.create_new_connection(connection, connected_node_id, client_address[0],
                                                           client_address[1])
                thread_client.start()

                message = {"type": "resource", "content": self.resources, "to": connected_node_id}
                thread_client.send(message)

                self.nodes_inbound.append(thread_client)

                self.inbound_node_connected(thread_client)

            except socket.timeout:
                pass
                # self.logger.warning('Node: Connection timeout!')

            except Exception as e:
                self.logger.error(str(e))

        self.logger.debug("Node stopping...")
        self.shutdown()
        self.logger.info("Node stopped")

    def stop(self):
        self.node_request_to_stop()
        self.terminate_flag.set()

    def shutdown(self):
        for t in self.nodes_inbound:
            t.send({"type": "shutdown"})
            # t.sock.shutdown(2)
            t.sock.close()
            t.stop()

        for t in self.nodes_outbound:
            t.send({"type": "shutdown"})
            # t.sock.shutdown(2)
            t.sock.close()
            t.stop()

        time.sleep(1)

        for t in self.nodes_inbound:
            t.join()

        for t in self.nodes_outbound:
            t.join()

        self.sock.settimeout(None)
        self.sock.close()

    def connect_with_node(self, host, port):
        if host == self.host and port == self.port:
            self.logger.warning("connect_with_node: Cannot connect with yourself!!")
            return None

        for node in self.nodes_outbound:
            if node.host == host and node.port == port:
                self.logger.info("connect_with_node: Already connected with this node.")
                return node

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.debug("connecting to %s port %s" % (host, port))
            sock.connect((host, port))

            sock.send(self.id.encode('utf-8'))
            connected_node_id = sock.recv(4096).decode('utf-8')

            thread_client = self.create_new_connection(sock, connected_node_id, host, port)
            thread_client.start()

            message = {"type": "resource", "content": self.resources, "to": connected_node_id}
            thread_client.send(message)
            self.nodes_outbound.append(thread_client)
            self.outbound_node_connected(thread_client)
            return thread_client

        except Exception as e:
            raise e

    def delete_closed_connections(self):
        for n in self.nodes_inbound:
            if n.terminate_flag.is_set() or n.sock._closed:
                self.inbound_node_disconnected(n)
                n.join()
                del self.nodes_inbound[self.nodes_inbound.index(n)]
                if n.id in self.neighbors:
                    self.neighbors.pop(n.id)

        for n in self.nodes_outbound:
            if n.terminate_flag.is_set() or n.sock._closed:
                self.outbound_node_disconnected(n)
                n.join()
                del self.nodes_outbound[self.nodes_outbound.index(n)]
                if n.id in self.neighbors:
                    self.neighbors.pop(n.id)

    def node_message(self, node, message):
        type = message["type"]
        self.logger.info(f"message {type} received from node {message['from']}")
        if message["to"] != self.id:
            self.logger.info(f"Forward Message to node {message['to']}")
            self.send_to_node_by_id(message["to"], message)
        else:
            self.logger.debug(f"Message Received: {message}")
            if type == "resource":
                self.neighbors[message["from"]] = message["content"]
            elif type == "result":
                res = message["content"]
                self.logger.info(f"result received for {message['request']} - {res}")
            elif type in self.resources:
                self.logger.info(f"do action {type}")
                self.do_action(message)
            else:
                self.logger.info(f"Forward request {type} to others")
                self.send_to_node_with_resource(message)

    def send_to_node(self, n, data):
        if n in self.all_nodes:
            try:
                n.send(data)
                self.logger.debug(f"Message {data} sent")
                return True

            except Exception as e:
                self.logger.error(str(e))
        else:
            self.logger.error(f"Node {n.id} not connected")

        return False

    def send_to_node_with_resource(self, data):
        self.delete_closed_connections()
        for id, resources in self.neighbors.items():
            if data["type"] in resources:
                self.logger.info(f"find resource in node {id}")
                data["to"] = id
                return self.send_to_node_by_id(id, data)

        self.logger.warning("Unknown node having resource, send to neighbor instead")
        n = self.choose_random_neighbor(exclude=[data.get("origin"), data.get("from")])
        if n is not None:
            if self.send_to_node(n, data):
                self.logger.info(f"Message sent to node {n.id}")
                return True
            else:
                return False

        self.logger.error(f"No available nodes")
        return False

    def send_to_node_by_id(self, id, data):
        self.delete_closed_connections()
        for n in self.all_nodes:
            if n.id == id:
                if self.send_to_node(n, data):
                    self.logger.info(f"Message sent to node {n.id}")
                    return True
                else:
                    return False

        self.logger.warning("Unknown node of id, send to neighbor instead")
        n = self.choose_random_neighbor(exclude=[data.get("origin"), data.get("from")])
        if n is not None:
            if self.send_to_node(n, data):
                self.logger.info(f"Message sent to node {n.id}")
                return True
            else:
                return False

        self.logger.error(f"Fail to send to node {id}")
        return False

    def choose_random_neighbor(self, exclude=None):
        self.delete_closed_connections()
        idxs = list(range(len(self.all_nodes)))
        random.shuffle(idxs)
        for idx in idxs:
            n = self.all_nodes[idx]
            if n.id not in exclude:
                return n

    def do_action(self, data):
        action = data['type']
        if action in self.resources:
            message = {"type": "result", "to": data["origin"], "origin": self.id,
                       "request": data["id"]}
            try:
                results = self.modules[action].main(data["content"])
                self.logger.debug(f"action {action} results - {results}")
                if results is not None:
                    message["content"] = results
            except Exception as e:
                message["content"] = {"error": str(e)}
            self.send_to_node_by_id(data["origin"], message)
            return True
        else:
            self.logger.error("None available module")
            return False

    def outbound_node_connected(self, node):
        self.logger.info("outbound_node_connected: " + node.id)

    def inbound_node_connected(self, node):
        self.logger.info("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
        self.logger.info("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        self.logger.info("outbound_node_disconnected: " + node.id)

    def node_disconnect_with_outbound_node(self, node):
        self.logger.debug("node wants to disconnect with other outbound node: " + node.id)

    def node_request_to_stop(self):
        self.logger.debug("node is requested to stop!")
