import sqlite3

DB_PATH = "voting-system-admin.sqlite"


class DAL:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.con = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.con.cursor()
        self.create_tables_if_needed()

    def create_tables_if_needed(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS campaigns"
                            "(campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "remote_campaign_id INTEGER,"
                            "name TEXT,"
                            "public_key TEXT,"
                            "private_key TEXT)")

    def add_campaign(self, remote_campaign_id, campaign_name, public_key, private_key):
        self.cursor.execute(
            "INSERT INTO campaigns (remote_campaign_id, name, public_key, private_key)"
            "VALUES (?, ?, ?, ?)",
            (remote_campaign_id, campaign_name, public_key, private_key)
        )
        self.con.commit()

    def get_campaign_info(self, remote_campaign_id):
        campaign = self.cursor.execute("SELECT * FROM campaigns WHERE remote_campaign_id=?",
                                       (remote_campaign_id,)).fetchone()
        return {
            "campaign_id": campaign[0],
            "remote_campaign_id": campaign[1],
            "name": campaign[2],
            "public_key": campaign[3],
            "private_key": campaign[4]
        }
