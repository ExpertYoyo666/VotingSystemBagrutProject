import json
import unittest
import sqlite3
import os
from time import time

from DAL import DAL


class TestDAL(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_voting_system.sqlite"
        self.dal = DAL()
        self.dal.db_path = self.test_db
        self.dal.con = sqlite3.connect(self.test_db)
        self.dal.cursor = self.dal.con.cursor()
        self.dal.create_tables_if_needed()

    def tearDown(self):
        self.dal.con.close()
        os.remove(self.test_db)

    def test_create_tables_if_needed(self):
        self.dal.create_tables_if_needed()
        self.dal.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.dal.cursor.fetchall()
        expected_tables = [('voters',), ('admins',), ('campaigns',)]
        self.assertTrue(all(table in tables for table in expected_tables))

    def test_add_campaign(self):
        self.dal.add_campaign("Test Campaign", 1000, 2000, "public key1234", "private key4321")
        self.dal.cursor.execute("SELECT * FROM campaigns WHERE name='Test Campaign'")
        campaign = self.dal.cursor.fetchone()

        self.assertIsNotNone(campaign)
        self.assertEqual(campaign[1], "Test Campaign")
        self.assertEqual(campaign[2], 1000)
        self.assertEqual(campaign[3], 2000)
        self.assertEqual(campaign[4], "public key1234")
        self.assertEqual(campaign[5], "private key4321")

        self.dal.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.dal.cursor.fetchall()
        expected_tables = [('voters',), ('admins',), ('campaigns',)]
        self.assertTrue(all(table in tables for table in expected_tables))

    def test_add_voter(self):
        self.dal.add_voter("test_user", "test_password")
        self.dal.cursor.execute("SELECT * FROM voters WHERE username='test_user'")
        voter = self.dal.cursor.fetchone()
        self.assertIsNotNone(voter)
        self.assertEqual(voter[1], "test_user")
        self.assertEqual(voter[2], "test_password")
        self.assertEqual(voter[3], "test_public_key")

    def test_add_admin(self):
        self.dal.add_admin("admin_user", "admin_password")
        self.dal.cursor.execute("SELECT * FROM admins WHERE username='admin_user'")
        admin = self.dal.cursor.fetchone()
        self.assertIsNotNone(admin)

        self.assertEqual(admin[1], "admin_user")
        self.assertEqual(admin[2], "admin_password")

    def test_create_campaign_tables(self):
        self.dal.create_campaign_tables(1)
        self.dal.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'votes_1'")
        votes_table = self.dal.cursor.fetchone()
        self.assertIsNotNone(votes_table)

    def test_get_voter(self):
        self.dal.add_voter("test_user", "test_password")
        voter_id = self.dal.get_voter("test_user")
        self.assertIsNotNone(voter_id)

    def test_get_admin(self):
        self.dal.add_admin("admin_user", "admin_password")
        admin_id = self.dal.get_admin("admin_user")
        self.assertIsNotNone(admin_id)

    def test_add_vote(self):
        self.dal.create_campaign_tables(1)
        self.dal.add_vote("test_nonce", 2, 1, "encrypted_vote")
        self.dal.cursor.execute("SELECT * FROM votes_1 WHERE nonce='test_nonce'")
        vote = self.dal.cursor.fetchone()
        self.assertIsNotNone(vote)

        self.assertEqual(vote[0], "test_nonce")
        self.assertEqual(vote[1], 2)
        self.assertEqual(vote[2], "encrypted_vote")
        self.assertEqual(vote[3], int(time()))

    def test_get_encrypted_votes_batch(self):
        self.dal.create_campaign_tables(1)
        vote = {
            "type": "VOTE_REQUEST",
            "encrypted_vote": "hi",
            "signature": "bomba",
            "nonce": "hi",
            "voter_id": 2,
            "campaign_id": 1
        }

        self.dal.add_vote("test_nonce", 2, 1, json.dumps(vote))
        votes = self.dal.get_encrypted_votes_batch(1, 10, 0)
        self.assertEqual(len(votes), 1)

    def test_get_total_votes_count(self):
        self.dal.create_campaign_tables(1)
        self.dal.add_vote("test_nonce", 2, 1, "encrypted_vote")
        total_votes = self.dal.get_total_votes_count(1)
        self.assertEqual(total_votes, 1)

    def test_store_aggregated_tally(self):
        self.dal.create_campaign_tables(1)
        self.dal.store_aggregated_tally(1, 1, "encrypted_tally")
        self.dal.cursor.execute("SELECT * FROM aggregated_votes_1 WHERE nominee_id=1")
        tally = self.dal.cursor.fetchone()
        self.assertIsNotNone(tally)
        self.assertEqual(tally[1], "encrypted_tally")

    def test_get_aggregated_tallies(self):
        self.dal.create_campaign_tables(1)
        self.dal.store_aggregated_tally(1, 1, "encrypted_tally")
        tallies = self.dal.get_aggregated_tallies(1)
        self.assertIn(1, tallies)
        self.assertEqual(tallies[1], "encrypted_tally")

    # def test_create_voter(self):
    #     """Tests voter account creation"""
    #     dal = DAL()
    #     if not table_exists("voters", dal):
    #         self.skipTest("voters table doesn't exist")
    #     dal.add_voter_account(0, "yoyo", "123435678")
    #     result = dal.cursor.execute(f"SELECT * FROM voters")
    #
    # def test_create_admin(self):
    #     """Tests admin account creation"""
    #     dal = DAL()
    #     if not table_exists("admins", dal):
    #         self.skipTest("admins table doesn't exist")
    #     dal.add_admin_account(0, "yoyo", "123435678")
    #     result = dal.cursor.execute(f"SELECT * FROM admins")


if __name__ == '__main__':
    unittest.main(verbosity=2)
