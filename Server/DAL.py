import json
import sqlite3
from time import time

import bcrypt

DB_PATH = "voting-system.sqlite"


class DAL:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.con = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.con.cursor()
        self.create_tables_if_needed()

    def create_tables_if_needed(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS voters (
                voter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                public_key TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                id TEXT UNIQUE,
                start_timestamp INT,
                end_timestamp INT,
                is_activated INT,
                public_key TEXT
            )
        """)
        self.con.commit()

        # Add Admin account to allow system access
        default_admin_username = "admin"
        default_admin_password = "admin"
        if self.get_admin(default_admin_username) is None:
            hashed_password = bcrypt.hashpw(default_admin_password.encode(), bcrypt.gensalt())
            self.add_admin(default_admin_username, hashed_password)

    def create_campaign_tables(self, campaign_id):
        self.cursor.execute(
            f"""CREATE TABLE votes_{campaign_id} ( 
                 voter_id INTEGER PRIMARY KEY,
                 encrypted_vote TEXT,
                 receipt TEXT,
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
                nonce TEXT PRIMARY KEY)""")

    def add_campaign(self, campaign_name, campaign_id, start_timestamp, end_timestamp, public_key):
        self.cursor.execute(
            "INSERT INTO campaigns (name, id, start_timestamp, end_timestamp, is_activated, public_key)"
            "VALUES (?, ?, ?, ?, ?, ?)",
            (campaign_name, campaign_id, start_timestamp, end_timestamp, 0, public_key)
        )
        self.con.commit()
        self.create_campaign_tables(self.cursor.lastrowid)

    def activate_campaign(self, campaign_id):
        self.cursor.execute(
            "UPDATE campaigns SET is_activated = 1 WHERE campaign_id = ?", (campaign_id,)
        )
        self.con.commit()

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

    def add_vote(self, nonce, voter_id, campaign_id, receipt, encrypted_vote):
        self.cursor.execute(
            f"INSERT INTO votes_{campaign_id} (voter_id, encrypted_vote, receipt, vote_timestamp)"
            "VALUES (?, ?, ?, ?)",
            (voter_id, encrypted_vote, receipt, int(time()))
        )
        self.cursor.execute(
            f"INSERT INTO nonces_{campaign_id} (nonce) VALUES (?)", (nonce,))
        self.con.commit()

    def add_nominee_to_campaign(self, campaign_id, nominee_name):
        self.cursor.execute(f"INSERT INTO campaign_nominees_{campaign_id} (nominee_name) VALUES (?)",
                            (nominee_name,))
        self.con.commit()

    def assign_voter_to_campaign(self, voter_id, campaign_id):
        self.cursor.execute(f"INSERT INTO campaign_voters_{campaign_id} (voter_id, has_voted) VALUES (?, ?)",
                            (voter_id, 0))
        self.con.commit()

    def set_voter_has_voted(self, voter_id, campaign_id):
        self.cursor.execute(f"UPDATE campaign_voters_{campaign_id} SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        self.con.commit()

    def get_voter_has_voted(self, voter_id, campaign_id):
        self.cursor.execute(f"SELECT has_voted FROM campaign_voters_{campaign_id} WHERE voter_id = ?", (voter_id,))
        return self.cursor.fetchone()[0]

    def add_nonce(self, nonce, campaign_id):
        self.cursor.execute(f"INSERT INTO nonces_{campaign_id} VALUES (?)", (nonce,))
        self.con.commit()

    def nonce_exists(self, nonce, campaign_id):
        self.cursor.execute(f"SELECT EXISTS (SELECT 1 FROM nonces_{campaign_id} WHERE nonce = ?)", (nonce,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def get_voter(self, username):
        self.cursor.execute("SELECT * FROM voters WHERE username=(?)", (username,))
        return self.cursor.fetchone()

    def get_admin(self, username):
        self.cursor.execute("SELECT * FROM admins WHERE username=(?)", (username,))
        return self.cursor.fetchone()

    def get_campaign_info(self, campaign_id):
        campaign_info = self.cursor.execute(f"SELECT * FROM campaigns"
                                            f" WHERE campaign_id={campaign_id}").fetchone()

        nominees = self.cursor.execute(f"SELECT * FROM campaign_nominees_{campaign_id}").fetchall()
        nominees = [row for row in nominees]

        voter_count = self.cursor.execute(
            f"SELECT COUNT(*) FROM campaign_voters_{campaign_id}").fetchone()[0]

        votes_count = self.cursor.execute(
            f"SELECT COUNT(*) FROM votes_{campaign_id}").fetchone()[0]

        return {
            "campaign_id": campaign_info[0],
            "name": campaign_info[1],
            "id": campaign_info[2],
            "start_timestamp": campaign_info[3],
            "end_timestamp": campaign_info[4],
            "is_active": campaign_info[5],
            "public_key": campaign_info[6],
            "nominees": nominees,
            "voters": voter_count,
            "votes": votes_count
        }

    def get_campaign_list(self, voter_id, is_admin):
        self.cursor.execute("SELECT campaign_id, id, name, start_timestamp, end_timestamp FROM campaigns")
        all_campaigns = self.cursor.fetchall()
        if is_admin:
            return all_campaigns

        campaigns = []

        for campaign in all_campaigns:
            campaign_id = campaign[0]
            voter_count = self.cursor.execute(
                f"SELECT COUNT(*) FROM campaign_voters_{campaign_id} WHERE voter_id=?", (voter_id,)).fetchone()[0]
            is_activated = self.get_campaign_info(campaign_id)['is_active']
            if voter_count > 0 and is_activated:
                campaigns.append(campaign)

        return campaigns

    def get_encrypted_votes_batch(self, campaign_id, batch_size, offset):
        self.cursor.execute(
            f"SELECT encrypted_vote FROM votes_{campaign_id} LIMIT {batch_size} OFFSET {offset}")
        return [json.loads(row[0]) for row in self.cursor.fetchall()]

    def get_total_votes_count(self, campaign_id):
        self.cursor.execute(f"SELECT COUNT(*) FROM votes_{campaign_id}")
        return self.cursor.fetchone()[0]

    def store_aggregated_tally(self, campaign_id, nominee_id, encrypted_tally):
        encrypted_tally_hex = hex(encrypted_tally)
        self.cursor.execute(
            f"INSERT OR REPLACE INTO aggregated_votes_{campaign_id} VALUES (?, ?)", (nominee_id, encrypted_tally_hex)
        )
        self.con.commit()

    def get_public_key(self, voter_id):
        self.cursor.execute("SELECT public_key FROM voters WHERE voter_id=?", (voter_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_aggregated_tallies(self, campaign_id):
        self.cursor.execute(f"SELECT nominee_id, encrypted_tally FROM aggregated_votes_{campaign_id}")
        return {row[0]: int(row[1], 16) for row in self.cursor.fetchall()}
