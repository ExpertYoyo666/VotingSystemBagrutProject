import json
import ssl
import struct
from enum import Enum
import socket

HOST = '127.0.0.1'
PORT = 1234

START_MARKER = b'\x01\x02'
END_MARKER = b'\x03\x04'

CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'


class RequestType(Enum):
    AUTH_REQUEST = "AUTH_REQUEST"
    AUTH_RESPONSE = "AUTH_RESPONSE"
    CAMPAIGN_INFO_REQUEST = "CAMPAIGN_INFO_REQUEST"
    CAMPAIGN_INFO_RESPONSE = "CAMPAIGN_INFO_RESPONSE"
    VOTE_REQUEST = "VOTE_REQUEST"
    VOTE_RESPONSE = "VOTE_RESPONSE"
    CAMPAIGN_LIST_REQUEST = "CAMPAIGN_LIST_REQUEST"
    CAMPAIGN_LIST_RESPONSE = "CAMPAIGN_LIST_RESPONSE"
    ADMIN_AUTH_REQUEST = "ADMIN_AUTH_REQUEST"
    ADMIN_AUTH_RESPONSE = "ADMIN_AUTH_RESPONSE"
    ADD_CAMPAIGN_REQUEST = "ADD_CAMPAIGN_REQUEST"
    ACTIVATE_CAMPAIGN_REQUEST = "ACTIVATE_CAMPAIGN_REQUEST"
    ASSIGN_VOTER_TO_CAMPAIGN_REQUEST = "ASSIGN_VOTER_TO_CAMPAIGN_REQUEST"
    ADD_VOTER_REQUEST = "ADD_VOTER_REQUEST"
    ADD_NOMINEE_REQUEST = "ADD_NOMINEE_REQUEST"
    GET_RESULTS_REQUEST = "GET_RESULTS_REQUEST"
    GET_RESULTS_RESPONSE = "GET_RESULTS_RESPONSE"

    GENERIC_RESPONSE = "GENERIC_RESPONSE"


class Protocol:
    def __init__(self):
        self.sock = None
        self.connect_to_server()

    def connect_to_server(self):
        # create context for ssl
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # create connection
        sock = socket.create_connection((HOST, PORT))
        sock.settimeout(1)
        # add ssl
        wrapped_sock = context.wrap_socket(sock, server_hostname=HOST)
        self.sock = wrapped_sock

    def recvall(self, n):
        """Receives n bytes from server"""
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_message(self, message):
        # encode message as json
        message = json.dumps(message).encode('utf-8')
        # add start and end markers, convert message length to bytes
        msg = (START_MARKER +
               struct.pack('>I', len(message)) +
               message +
               END_MARKER)
        # send message to server
        try:
            self.sock.sendall(msg)
        except ssl.SSLEOFError:
            raise ConnectionError("Server Disconnected")

    def receive_server_response(self):
        try:
            # read and validate the start marker
            if self.recvall(len(START_MARKER)) != START_MARKER:
                return

            # read the message length
            raw_msg_len = self.recvall(4)
            if not raw_msg_len:
                return
            msg_len = struct.unpack('>I', raw_msg_len)[0]

            # read the message payload
            payload = json.loads(self.recvall(msg_len).decode('utf-8'))

            # read and validate the end marker
            if self.recvall(len(END_MARKER)) != END_MARKER:
                return

            print(f"Received: {payload}")
            return payload
        except ConnectionResetError:
            return

    def auth(self, username, password):
        request = {
            "type": RequestType.ADMIN_AUTH_REQUEST.value,
            "username": username,
            "password": password
        }

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.ADMIN_AUTH_RESPONSE.value and response["status"] == "SUCCESS":
            return True, ""
        return False, response["reason"]

    def get_campaigns_list(self):
        # create request
        request = {
            "type": RequestType.CAMPAIGN_LIST_REQUEST.value
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.CAMPAIGN_LIST_RESPONSE.value:
            return response["campaigns"]
        return []

    def get_campaign_info(self, campaign_id):
        # create request
        request = {
            "type": RequestType.CAMPAIGN_INFO_REQUEST.value,
            "campaign_id": campaign_id
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.CAMPAIGN_INFO_RESPONSE.value:
            return response
        return []

    def add_campaign(self, campaign_name, uid, start_timestamp, end_timestamp, public_key):
        # create request
        request = {
            "type": RequestType.ADD_CAMPAIGN_REQUEST.value,
            "name": campaign_name,
            "id": uid,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "public_key": public_key
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.GENERIC_RESPONSE.value and response["status"] == "SUCCESS":
            return True, ""
        return False, response["reason"]

    def activate_campaign(self, campaign_id):
        # create request
        request = {
            "type": RequestType.ACTIVATE_CAMPAIGN_REQUEST.value,
            "campaign_id": campaign_id
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.GENERIC_RESPONSE.value and response["status"] == "SUCCESS":
            return True, ""
        return False, response["reason"]

    def add_voter(self, voter_name, voter_password):
        # create request
        request = {
            "type": RequestType.ADD_VOTER_REQUEST.value,
            "username": voter_name,
            "password": voter_password,
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.GENERIC_RESPONSE.value and response["status"] == "SUCCESS":
            return True, ""
        return False, response["reason"]

    def add_voter_to_campaign(self, voter_name, campaign_id):
        # create request
        request = {
            "type": RequestType.ASSIGN_VOTER_TO_CAMPAIGN_REQUEST.value,
            "voter_name": voter_name,
            "campaign_id": campaign_id,
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.GENERIC_RESPONSE.value and response["status"] == "SUCCESS":
            return True, ""
        return False, response["reason"]

    def add_nominee_to_campaign(self, nominee_name, campaign_id):
        # create request
        request = {
            "type": RequestType.ADD_NOMINEE_REQUEST.value,
            "name": nominee_name,
            "campaign_id": campaign_id,
        }

        self.send_message(request)

        response = self.receive_server_response()

        # check success
        if response["type"] == RequestType.GENERIC_RESPONSE.value and response["status"] == "SUCCESS":
            return True, ""
        return False, response["reason"]

    def get_campaign_results(self, campaign_id):
        request = {
            "type": RequestType.GET_RESULTS_REQUEST.value,
            "campaign_id": campaign_id
        }

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.GET_RESULTS_RESPONSE.value:
            return response["results"]
        return []
