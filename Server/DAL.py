import json
import sqlite3
from time import time

DB_PATH = ".//db//db.db"


class DAL:
    def __init__(self):
        self.db_path = DB_PATH
        self.con = sqlite3.connect(self.db_path)
        self.cursor = self.con.cursor()
        # self.create_tables()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS voters"
                            "(PRIMARY KEY voter_id INT, username TEXT , password TEXT, public_key TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS admins"
                            "(PRIMARY KEY admin_id INT, username TEXT , password TEXT, public_key TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS campaigns"
                            "(PRIMARY KEY campaign_id INT, opening_timestamp INT, closing_timestamp INT, campaign_name TEXT)")

    def create_campaign_tables(self, campaign_id):
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS votes_{campaign_id} (
             PRIMARY KEY nonce TEXT, 
             voter_id TEXT,
             encrypted_vote TEXT,
             vote_timestamp INTEGER,
             FOREIGN KEY (voter_id) REFERENCES voters(voter_id))"""
        )
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS aggregated_votes_{campaign_id} (
                            PRIMARY KEY candidate_id INTEGER, 
                            encrypted_tally TEXT)"""
        )

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS campaign_voters_{campaign_id} (
                            PRIMARY KEY voter_id INTEGER
                            has_voted INTEGER)"""
        )

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS campaign_nominees_{campaign_id} (
                                PRIMARY KEY nominee_id INTEGER, 
                                nominee_name TEXT,
                                description TEXT)"""
        )

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS nonces_{campaign_id} (
                                PRIMARY KEY nonce)""")

    def add_campaign(self, campaign_id, campaign_name):
        self.cursor.execute(
            f"INSERT INTO campaigns (campaign_id, name) VALUES ({campaign_id}, {campaign_name})",
        )
        self.create_campaign_tables(campaign_id)

    def add_voter(self, voter_id, public_key):
        self.cursor.execute(
            f"INSERT INTO voters (voter_id, public_key) VALUES ({voter_id}, {public_key})"
        )

    def add_vote(self, campaign_id, nonce, voter_id, encrypted_vote):
        self.cursor.execute(
            f"INSERT INTO votes_{campaign_id} (nonce, voter_id, encrypted_vote) VALUES"
            f" ({nonce}, {voter_id}, {encrypted_vote}, {time()})",
        )

    def add_nominee_to_campaign(self, nominee_id, campaign_id, nominee_name, description):
        self.cursor.execute(f"INSERT INTO campaign_nominees_{campaign_id} VALUES ({nominee_id}, {nominee_name}, {description})")

    def assign_voter_to_campaign(self, voter_id, campaign_id):
        self.cursor.execute(f"INSERT INTO campaign_voters_{campaign_id} VALUES ({voter_id})")

    def add_nonce(self, nonce, campaign_id):
        self.cursor.execute(f"INSERT INTO nonces_{campaign_id} VALUES ({nonce})")

    def nonce_exists(self, nonce, campaign_id):
        self.cursor.execute(f"SELECT exists FROM nonces_{campaign_id} where nonce={nonce})")

    def get_encrypted_votes_batch(self, campaign_id, batch_size, offset):
        self.cursor.execute(
            f"SELECT encrypted_vote FROM votes_{campaign_id} LIMIT {batch_size} OFFSET {offset}")
        return [json.loads(row[0]) for row in self.cursor.fetchall()]  # [0]?

    def get_total_votes_count(self, campaign_id):
        self.cursor.execute(f"SELECT COUNT(*) FROM votes_{campaign_id}")
        return self.cursor.fetchone()[0]

    def store_aggregated_tally(self, campaign_id, candidate_id, encrypted_tally):
        self.cursor.execute(
            f"INSERT OR REPLACE INTO aggregated_votes_{campaign_id} VALUES ({candidate_id}, {encrypted_tally})"
        )

    def get_public_key(self, voter_id):
        self.cursor.execute(f"SELECT public_key FROM voters WHERE voter_id={voter_id}")
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_aggregated_tallies(self, campaign_id):
        self.cursor.execute(f"SELECT candidate_id, encrypted_tally FROM aggregated_votes_{campaign_id}")
        return {row[0]: row[1] for row in self.cursor.fetchall()}


if __name__ == '__main__':
    dbm = DAL()  # DAL = Data Abstraction Layer
