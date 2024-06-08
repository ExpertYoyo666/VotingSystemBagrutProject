import unittest
from DAL import DAL
import sqlite3


def table_exists(table_name, dal):
    return bool(
        dal.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'").fetchall())


class TestDAL(unittest.TestCase):
    def test_create_voter(self):
        """Tests voter account creation"""
        dal = DAL()
        if not table_exists("voters", dal):
            self.skipTest("voters table doesn't exist")
        dal.add_voter_account(0, "yoyo", "123435678")
        result = dal.cursor.execute(f"SELECT * FROM voters")

    def test_create_admin(self):
        """Tests admin account creation"""
        dal = DAL()
        if not table_exists("admins", dal):
            self.skipTest("admins table doesn't exist")
        dal.add_admin_account(0, "yoyo", "123435678")
        result = dal.cursor.execute(f"SELECT * FROM admins")


if __name__ == '__main__':
    unittest.main(verbosity=2)
