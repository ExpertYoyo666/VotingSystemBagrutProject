import json
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import phe.paillier as paillier


class Vote:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.paillier_public_key = None
        self.generate_keys()

    def generate_keys(self):
        # Generate RSA key pair for signing votes
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def get_public_key_pem(self):
        # Serialize the public key to PEM format for registration
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        return public_pem

    def set_paillier_public_key(self, paillier_public_key):
        self.paillier_public_key = paillier.PaillierPublicKey(int(paillier_public_key))

    def create_vote(self, campaign_id, candidate_index, num_candidates):
        if self.paillier_public_key is None:
            raise Exception('Paillier public key is not set')

        # Generate a unique nonce for the vote
        nonce = str(uuid.uuid4())

        # Create the vote vector (e.g., [0, 0, 1, 0] for candidate 3 out of 4)
        vote = [1 if i == candidate_index else 0 for i in range(num_candidates)]

        # Encrypt the vote
        encrypted_vote = [self.paillier_public_key.encrypt(v) for v in vote]

        # Create the data to be signed
        data_to_sign = {
            "encrypted_vote": [ev.ciphertext() for ev in encrypted_vote],
            "nonce": nonce,
            "campaign_id": campaign_id
        }

        print(json.dumps(data_to_sign).encode())

        # Sign the data
        signature = self.private_key.sign(
            json.dumps(data_to_sign).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Create the vote message
        vote_message = {
            "encrypted_vote": [ev.ciphertext() for ev in encrypted_vote],
            "nonce": nonce,
            "campaign_id": campaign_id,
            "signature": signature.hex(),
            "public_key": self.get_public_key_pem()
        }

        return vote_message