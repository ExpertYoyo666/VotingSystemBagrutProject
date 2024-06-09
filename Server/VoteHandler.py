import json
import phe.paillier as paillier
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


# Generate Paillier keys
def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key


# Validate a vote
def validate_vote_signature(vote_message, public_key_pem):
    encrypted_vote = [int(ev) for ev in vote_message['encrypted_vote']]
    signature = bytes.fromhex(vote_message['signature'])
    voter_id = vote_message['voter_id']
    nonce = vote_message['nonce']
    campaign_id = vote_message['campaign_id']

    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    try:
        public_key.verify(
            signature,
            json.dumps(encrypted_vote).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except:
        raise ValueError("Invalid vote signature.")

    return True


# Aggregate votes
def tally_votes_in_batches(dal, campaign_id, public_key, batch_size=1000):
    total_votes_count = dal.get_total_votes_count(campaign_id)
    num_batches = (total_votes_count // batch_size) + (1 if total_votes_count % batch_size != 0 else 0)

    if total_votes_count == 0:
        print("No votes to tally.")
        return

    num_candidates = len(json.loads(dal.get_encrypted_votes_batch(campaign_id, 1, 0)[0]))
    encrypted_tallies = [paillier.EncryptedNumber(public_key, 0) for _ in range(num_candidates)]

    for batch_num in range(num_batches):
        print(f"Processing batch {batch_num + 1} of {num_batches}")
        encrypted_votes_batch = dal.get_encrypted_votes_batch(campaign_id, batch_size, batch_num * batch_size)

        for vote in encrypted_votes_batch:
            for i in range(num_candidates):
                encrypted_tallies[i] += paillier.EncryptedNumber(public_key, vote[i])

    for i, tally in enumerate(encrypted_tallies):
        dal.store_aggregated_tally(campaign_id, i, tally.ciphertext())


# Decrypt results
def decrypt_results(dal, campaign_id, private_key):
    encrypted_tallies = dal.get_aggregated_tallies(campaign_id)
    total_votes = {i: private_key.decrypt(paillier.EncryptedNumber(private_key.public_key(), int(tally))) for i, tally
                   in encrypted_tallies.items()}
    for i, tally in total_votes.items():
        print(f"Total votes for candidate {i + 1}: {tally}")