import json
import ssl
import struct
from enum import Enum
import socket

from Client.VotingClient.Vote import Vote

HOST = '127.0.0.1'
PORT = 1234

START_MARKER = b'\x01\x02'
END_MARKER = b'\x03\x04'

CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'


# enum for storing strings for request and response types
class RequestType(Enum):
    AUTH_REQUEST = "AUTH_REQUEST"
    AUTH_RESPONSE = "AUTH_RESPONSE"
    CAMPAIGN_INFO_REQUEST = "CAMPAIGN_INFO_REQUEST"
    CAMPAIGN_INFO_RESPONSE = "CAMPAIGN_INFO_RESPONSE"
    VOTE_REQUEST = "VOTE_REQUEST"
    VOTE_RESPONSE = "VOTE_RESPONSE"
    CAMPAIGN_LIST_REQUEST = "CAMPAIGN_LIST_REQUEST"
    CAMPAIGN_LIST_RESPONSE = "CAMPAIGN_LIST_RESPONSE"
    GENERIC_RESPONSE = "GENERIC_RESPONSE"


class Protocol:
    def __init__(self):
        self.sock = None
        self.connect_to_server()
        self.vote_handler = Vote()
        self.vote_handler.generate_keys()

    def connect_to_server(self):
        # init context for ssl
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # create ssl connection to server
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
        # encode message as json
        message = json.dumps(message).encode('utf-8')
        # add start and end markers and add message length as bytes
        msg = (START_MARKER +
               struct.pack('>I', len(message)) +
               message +
               END_MARKER)
        self.sock.sendall(msg)

    def receive_server_response(self):
        try:
            # read and validate the start marker
            if self.recvall(len(START_MARKER)) != START_MARKER:
                return

            # read the message length
            raw_msg_len = self.recvall(4)
            if not raw_msg_len:
                return
            # convert message length from bytes to int
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

    def get_campaigns_list(self):
        request = {
            "type": RequestType.CAMPAIGN_LIST_REQUEST.value
        }

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.CAMPAIGN_LIST_RESPONSE.value:
            return response["campaigns"]
        return []

    def get_campaign_info(self, campaign_id):
        request = {
            "type": RequestType.CAMPAIGN_INFO_REQUEST.value,
            "campaign_id": campaign_id
        }

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.CAMPAIGN_INFO_RESPONSE.value:
            return response["nominees"], response["public_key"]
        return [], None

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

    def vote(self, campaign_id, nominee_id, num_candidates, public_key):
        # set public key
        self.vote_handler.set_paillier_public_key(public_key)

        # create vote
        request = self.vote_handler.create_vote(campaign_id, nominee_id - 1, num_candidates)
        request["type"] = RequestType.VOTE_REQUEST.value

        self.send_message(request)

        response = self.receive_server_response()

        if response["type"] == RequestType.VOTE_RESPONSE.value:
            return response["status"], response["receipt"]
        return "FAIL", ""



