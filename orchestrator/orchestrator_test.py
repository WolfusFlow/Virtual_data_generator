import unittest
import os
import sqlalchemy

from database import db_string

class TestDB(unittest.TestCase):

    def setUp(self):

        if not db_string:
            self.skipTest("No database URL set")
        self.engine = sqlalchemy.create_engine(db_string)
        self.connection = self.engine.connect()
        self.connection.execute("CREATE DATABASE testdb")

    def tearDown(self):
        self.connection.execute("DROP DATABASE testdb")


if __name__ == '__main__':
    unittest.main()