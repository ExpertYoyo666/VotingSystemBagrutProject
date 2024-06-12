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
    ASSIGN_VOTER_TO_CAMPAIGN_REQUEST = "ASSIGN_VOTER_TO_CAMPAIGN_REQUEST"
    ADD_VOTER_REQUEST = "ADD_VOTER_REQUEST"
    ADD_NOMINEE_REQUEST = "ADD_NOMINEE_REQUEST"
    GET_RESULTS_REQUEST = "GET_RESULTS_REQUEST"

    GENERIC_RESPONSE = "GENERIC_RESPONSE"


class Protocol:
    def __init__(self):
        self.sock = None
        self.connect_to_server()

    def connect_to_server(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        sock = socket.create_connection((HOST, PORT))
        sock.settimeout(10)
        wrapped_sock = context.wrap_socket(sock, server_hostname=HOST)
        self.sock = wrapped_sock

    def recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_message(self, message):
        message = json.dumps(message).encode('utf-8')
        msg = (START_MARKER +
               struct.pack('>I', len(message)) +
               message +
               END_MARKER)
        self.sock.sendall(msg)

    def receive_server_response(self):
        try:
            # Read and validate the start marker
            if self.recvall(len(START_MARKER)) != START_MARKER:
                return

            # Read the message length
            raw_msg_len = self.recvall(4)
            if not raw_msg_len:
                return
            msg_len = struct.unpack('>I', raw_msg_len)[0]

            # Read the message payload
            payload = json.loads(self.recvall(msg_len).decode('utf-8'))

            # Read and validate the end marker
            if self.recvall(len(END_MARKER)) != END_MARKER:
                return

            print(f"Received: {payload}")
            return payload
        except ConnectionResetError:
            return

    def get_campaigns_list(self):
        request = {
            "type": RequestType.CAMPAIGN_LIST_REQUEST.value
        }

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.CAMPAIGN_LIST_RESPONSE.value:
            return response["campaigns"]
        return []

    def auth(self, username, password):
        request = {
            "type": RequestType.AUTH_REQUEST.value,
            "username": username,
            "password": password
        }

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.AUTH_RESPONSE.value and response["status"] == "SUCCESS":
            return True
        return False





