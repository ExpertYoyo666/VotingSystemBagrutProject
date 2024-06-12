import socket
import threading
import struct
import json
import ssl

from RequestHandler import RequestHandler

START_MARKER = b'\x01\x02'
END_MARKER = b'\x03\x04'

PORT = 1234
CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'


class Server:
    def __init__(self, dal):
        self.dal = dal
        self.request_handler = RequestHandler(self.dal)

    def handle_client(self, client_socket):
        state = {
            "is_auth": False,
            "is_admin": False
        }
        while True:
            try:
                # Read and validate the start marker
                if self.recvall(client_socket, len(START_MARKER)) != START_MARKER:
                    break

                # Read the message length
                raw_msg_len = self.recvall(client_socket, 4)
                if not raw_msg_len:
                    break
                msg_len = struct.unpack('>I', raw_msg_len)[0]

                # Read the message payload
                payload = self.recvall(client_socket, msg_len).decode('utf-8')

                # Read and validate the end marker
                if self.recvall(client_socket, len(END_MARKER)) != END_MARKER:
                    break

                print(f"Received: {payload}")
                response = self.request_handler.handle_request(payload, state)
                self.send_message(client_socket, response)
            except ConnectionResetError:
                break

        client_socket.close()

    def recvall(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_message(self, sock, message):
        message = json.dumps(message).encode('utf-8')
        msg = (START_MARKER +
               struct.pack('>I', len(message)) +
               message +
               END_MARKER)
        sock.sendall(msg)

    def main_loop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

        server.bind(('127.0.0.1', PORT))
        server.listen()

        while True:
            client_socket, address = server.accept()
            print(f"Accepted connection from {address}")
            wrapped_client_socket = context.wrap_socket(client_socket, server_side=True)
            client_handler_thread = threading.Thread(target=self.handle_client, args=(wrapped_client_socket,))
            client_handler_thread.start()
