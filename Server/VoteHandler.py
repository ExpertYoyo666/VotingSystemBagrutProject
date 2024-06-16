import json
import phe.paillier as paillier
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


# Generate Paillier keys
def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key


# Validate a vote
def validate_vote_signature(vote_message):
    encrypted_vote = [int(ev) for ev in vote_message['encrypted_vote']]
    nonce = vote_message['nonce']
    campaign_id = vote_message['campaign_id']
    signature = bytes.fromhex(vote_message['signature'])

    # public_key = serialization.load_pem_public_key(public_key_pem.encode())
    public_key = serialization.load_pem_public_key(vote_message["public_key"].encode('utf-8'))

    data_to_sign = {
        "encrypted_vote": encrypted_vote,
        "nonce": nonce,
        "campaign_id": campaign_id
    }

    try:
        public_key.verify(
            signature,
            json.dumps(data_to_sign).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except:
        return False

    return True


# Aggregate votes
def tally_votes_in_batches(dal, campaign_id, public_key_str, batch_size=1000):
    total_votes_count = dal.get_total_votes_count(campaign_id)
    num_batches = (total_votes_count // batch_size) + (1 if total_votes_count % batch_size != 0 else 0)

    public_key = paillier.PaillierPublicKey(int(public_key_str))

    if total_votes_count == 0:
        print("No votes to tally.")
        return

    encrypted_votes_batch = dal.get_encrypted_votes_batch(campaign_id, 1, 0)
    if not encrypted_votes_batch:
        print("No votes found in the first batch.")
        return

    num_candidates = len(encrypted_votes_batch[0])

    encrypted_tallies = [public_key.encrypt(0) for _ in range(num_candidates)]

    for batch_num in range(num_batches):
        encrypted_votes_batch = dal.get_encrypted_votes_batch(campaign_id, batch_size, batch_num * batch_size)

        for vote in encrypted_votes_batch:
            for i in range(num_candidates):
                encrypted_tallies[i] += paillier.EncryptedNumber(public_key, vote[i])

    for i, tally in enumerate(encrypted_tallies):
        dal.store_aggregated_tally(campaign_id, i, tally.ciphertext())

