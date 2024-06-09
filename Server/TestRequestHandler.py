import json
import unittest
import sqlite3
import os
from time import time

from DAL import DAL
from RequestHandler import RequestHandler, RequestType


class TestRequestHandler(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_voting_system.sqlite"
        self.dal = DAL(self.test_db)
        self.dal.create_tables_if_needed()

        self.handler = RequestHandler(self.dal)

    def tearDown(self):
        self.dal.con.close()
        os.remove(self.test_db)

    def test_request_handler(self):
        admin_auth_request = json.dumps({
            "type": RequestType.ADMIN_AUTH_REQUEST.value,
            "username": "admin",
            "password": "admin"
        })

        state = {
            "is_auth": False,
            "is_admin": False
        }

        self.handler.handle_request(admin_auth_request, state)

        self.assertTrue(state["is_auth"])
        self.assertTrue(state["is_admin"])

        add_campaign_request = json.dumps({
            "type": RequestType.ADD_CAMPAIGN_REQUEST.value,
            "name": "My Campaign",
            "start_timestamp": int(time()),
            "end_timestamp": int(time()) + 86400
        })

        self.handler.handle_request(add_campaign_request, state)

        campaigns = self.dal.get_campaign_list(None, state["is_admin"])
        self.assertIn("My Campaign", [row[1] for row in campaigns])

        voters = ["yoyo", "yoyo2", "oyoy"]
        for x in voters:
            add_voter_request = json.dumps({
                "type": RequestType.ADD_VOTER_REQUEST.value,
                "username": x,
                "password": "1234"
            })

            self.handler.handle_request(add_voter_request, state)

        for x in voters:
            voter_username = self.dal.get_voter(x)[1]
            self.assertEqual(voter_username, x)

        nominees = ["ido", "better_ido", "erez"]
        for x in nominees:
            add_nominee_request = json.dumps({
                "type": RequestType.ADD_NOMINEE_REQUEST.value,
                "campaign_id": 1,
                "name": x
            })

            self.handler.handle_request(add_nominee_request, state)

        for x in nominees:
            nominees_in_campaign = self.dal.get_campaign_info(1)[0]
            self.assertIn(x, [_[1] for _ in nominees_in_campaign])

















