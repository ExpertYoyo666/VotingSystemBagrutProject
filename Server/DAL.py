import json
import sqlite3
from time import time

DB_PATH = "voting-system.sqlite"


class DAL:
    def __init__(self):
        self.db_path = DB_PATH
        self.con = sqlite3.connect(self.db_path)
        self.cursor = self.con.cursor()
        self.create_tables_if_needed()

    def create_tables_if_needed(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS voters"
                            "(voter_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, public_key TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS admins"
                            "(admin_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")

        self.add_admin("admin", "admin")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS campaigns"
                            "(campaign_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, start_timestamp INT, end_timestamp INT,"
                            "public_key TEXT, private_key TEXT)")

    def create_campaign_tables(self, campaign_id):
        self.cursor.execute(
            f"""CREATE TABLE votes_{campaign_id} (
                 nonce TEXT PRIMARY KEY, 
                 voter_id INTEGER,
                 encrypted_vote TEXT,
                 vote_timestamp INTEGER)"""
        )

        self.cursor.execute(
            f"""CREATE TABLE aggregated_votes_{campaign_id} (
                nominee_id INTEGER PRIMARY KEY, 
                encrypted_tally TEXT)"""
        )

        self.cursor.execute(
            f"""CREATE TABLE campaign_voters_{campaign_id} (
                voter_id INTEGER PRIMARY KEY,
                has_voted INTEGER)"""
        )

        self.cursor.execute(
            f"""CREATE TABLE campaign_nominees_{campaign_id} (
                nominee_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nominee_name TEXT)"""
        )

        self.cursor.execute(
            f"""CREATE TABLE nonces_{campaign_id} (
                nonce INTEGER PRIMARY KEY)""")

    def add_campaign(self, campaign_name, start_timestamp, end_timestamp, public_key, private_key):
        self.cursor.execute(
            "INSERT INTO campaigns (name, start_timestamp, end_timestamp, public_key, private_key) VALUES (?, ?, ?, ?, ?)",
            (campaign_name, start_timestamp, end_timestamp, public_key, private_key)
        )
        self.con.commit()
        self.create_campaign_tables(self.cursor.lastrowid)

    def add_voter(self, username, password, public_key):
        self.cursor.execute(
            "INSERT INTO voters (username, password, public_key) VALUES (?, ?, ?)",
            (username, password, public_key)
        )
        self.con.commit()

    def add_admin(self, username, password):
        self.cursor.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            (username, password)
        )
        self.con.commit()

    def add_vote(self, nonce, voter_id, campaign_id, encrypted_vote):
        self.cursor.execute(
            f"INSERT INTO votes_{campaign_id} (nonce, voter_id, encrypted_vote, vote_timestamp) VALUES (?, ?, ?, ?)",
            (nonce, voter_id, encrypted_vote, int(time()))
        )
        self.con.commit()

    def add_nominee_to_campaign(self, campaign_id, nominee_name):
        self.cursor.execute(f"INSERT INTO campaign_nominees_{campaign_id} VALUES ({nominee_name})")

    def assign_voter_to_campaign(self, voter_id, campaign_id):
        self.cursor.execute(f"INSERT INTO campaign_voters_{campaign_id} VALUES ({voter_id})")

    def add_nonce(self, nonce, campaign_id):
        self.cursor.execute(f"INSERT INTO nonces_{campaign_id} VALUES ({nonce})")

    def nonce_exists(self, nonce, campaign_id):
        self.cursor.execute(f"SELECT EXISTS (SELECT * FROM nonces_{campaign_id} where nonce={nonce})")

    def get_voter(self, username):
        self.cursor.execute("SELECT * FROM voters WHERE username=(?)", (username,))
        return self.cursor.fetchone()[0]

    def get_admin(self, username):
        self.cursor.execute("SELECT * FROM admins WHERE username=(?)", (username,))
        return self.cursor.fetchone()[0]

    def get_campaign_info(self, campaign_id):
        nominees = self.cursor.execute(f"SELECT * FROM campaign_nominees_{campaign_id}").fetchall()
        nominees = [row[0] for row in nominees]

        public_key = self.cursor.execute(f"SELECT public_key FROM campaign"
                                         f" WHERE campaign_id={campaign_id}").fetchone()[0]
        return nominees, public_key

    def get_campaign_list(self, voter_id, is_admin):
        all_campaigns = self.cursor.execute(f"SELECT campaign_id FROM campaigns").fetchall()
        all_campaigns = [row[0] for row in all_campaigns]

        if not is_admin:
            campaigns = []
            for campaign_id in all_campaigns:
                if (campaign_info := self.cursor.execute(
                        f"SELECT * FROM campaign_voters_{campaign_id} WHERE voter_id={voter_id}").fetchone()):
                    campaigns.append((campaign_info[1], campaign_info[2], campaign_info[3], campaign_info[4]))

            return campaigns

        return all_campaigns

    def get_encrypted_votes_batch(self, campaign_id, batch_size, offset):
        self.cursor.execute(
            f"SELECT encrypted_vote FROM votes_{campaign_id} LIMIT {batch_size} OFFSET {offset}")
        return [json.loads(row[0]) for row in self.cursor.fetchall()]  # [0]?

    def get_total_votes_count(self, campaign_id):
        self.cursor.execute(f"SELECT COUNT(*) FROM votes_{campaign_id}")
        return self.cursor.fetchone()[0]

    def store_aggregated_tally(self, campaign_id, nominee_id, encrypted_tally):
        self.cursor.execute(
            f"INSERT OR REPLACE INTO aggregated_votes_{campaign_id} VALUES (?, ?)", (nominee_id, encrypted_tally)
        )

    def get_public_key(self, voter_id):
        self.cursor.execute(f"SELECT public_key FROM voters WHERE voter_id={voter_id}")
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_aggregated_tallies(self, campaign_id):
        self.cursor.execute(f"SELECT nominee_id, encrypted_tally FROM aggregated_votes_{campaign_id}")
        return {row[0]: row[1] for row in self.cursor.fetchall()}


if __name__ == '__main__':
    dbm = DAL()  # DAL = Data Abstraction Layer
