import unittest
import os
from main import get_weather, display_forecast, display_history, weather_query      # noqa
from dbscript import create_database, query_history, insert_history, delete_database     # noqa


class TestWithDatabase(unittest.TestCase):

    def setUp(self):
        # set up dummy database and entries before each test
        create_database('unittest.db')
        insert_history('unittest.db', "city1", "weather1")
        insert_history('unittest.db', "city2", "weather2")
        insert_history('unittest.db', "city3", "weather3")

    def tearDown(self):
        # clear dummy database after each test
        delete_database('unittest.db')

    def test_display_history(self):
        status = display_history('unittest.db')
        self.assertEqual(status, 0)

    def test_query_history(self):
        rows = query_history('unittest.db')
        self.assertEqual(len(rows), 3)

    def test_insert_history(self):
        insert_history('unittest.db', "city4", "weather4")
        rows = query_history('unittest.db')
        self.assertEqual(len(rows), 4)


# tests that don't require a database to be made beforehand
class TestNoSetUp(unittest.TestCase):
    def test_delete_database(self):
        create_database('to_delete.db')
        delete_database('to_delete.db')
        does_exist = os.path.exists('to_delete.db')
        self.assertFalse(does_exist)

    def test_create_database(self):
        create_database('dummy.db')
        does_exist = os.path.exists('dummy.db')
        self.assertTrue(does_exist)
        delete_database('dummy.db')


if __name__ == '__main__':
    unittest.main()
