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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " voters(PRIMARY KEY id INT, username TEXT , password TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " admins(PRIMARY KEY id INT, username TEXT , password TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " voter_campaign_assignments(PRIMARY KEY id INT, username TEXT, campaign TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " admin_campaign_assignments(PRIMARY KEY id INT, username TEXT, campaign TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " votes(PRIMARY KEY vote_timestamp INT, username TEXT, nominee TEXT, campaign TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " nominees(PRIMARY KEY id INT, nominee TEXT, description TEXT , campaignTEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS"
                            " campaigns(PRIMARY KEY id INT, opening_timestamp INT, closing_timestamp INT , campaign TEXT)")

    def add_user(self, id, username, password):
        self.cursor.execute(f"INSERT INTO voters VALUES ({id}, {username}, {password})")

    def add_admin(self, id, username, password):
        self.cursor.execute(f"INSERT INTO admins VALUES ({id}, {username}, {password})")

    def add_campaign(self, id, campaign, opening_time, closing_time):
        self.cursor.execute(f"INSERT INTO campaigns VALUES ({id}, {campaign}, {opening_time}, {closing_time})")

    def add_vote(self, username, nominee, campaign):
        self.cursor.execute(f"INSERT INTO votes VALUES ({username}, {nominee}, {campaign}, {time()})")

    def add_nominee(self, id, nominee, description, campaign):
        self.cursor.execute(f"INSERT INTO nominees VALUES ({id}, {nominee}, {description}, {campaign})")

    def assign_user_to_campaign(self, id, username, campaign):
        self.cursor.execute(f"INSERT INTO voter_campaign_assignments VALUES ({id}, {username}, {campaign})")

    def assign_admin_to_campaign(self, id, username, campaign,):
        self.cursor.execute(f"INSERT INTO admin_campaign_assignments VALUES ({id}, {username}, {campaign})")

    def get_nominees_for_campaign(self, campaign_name):
        return self.cursor.execute(f"SELECT nominee_name FROM nominees WHERE campaign_name={campaign_name}")

    def get_campaigns_for_user(self, username):
        return self.cursor.execute(f"SELECT campaign_name FROM campaigns WHERE username={username}")

    def get_results_for_campaign(self, campaign_name):
        return self.cursor.execute(f"SELECT * FROM votes WHERE campaign_name={campaign_name}")


if __name__ == '__main__':
    dbm = DAL()  # DAL = Data Abstraction Layer
