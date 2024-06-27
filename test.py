import unittest
import os
from main import get_weather, display_history, forecast_bars, Weather      # noqa
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

    def test_forecast_bars(self):
        weather1 = Weather(None, None, 1, None, None)
        weather2 = Weather(None, None, 2, None, None)
        weather3 = Weather(None, None, 3, None, None)

        bars = forecast_bars([weather1, weather2, weather3])
        self.assertTrue(isinstance(bars, list))


# tests responses to make sure they are of the correct data type.
class TestResponse(unittest.TestCase):
    def test_get_weather(self):
        test = get_weather("sterling")
        for i in test:

            # test that it returns a Weather and all getter functions operate
            self.assertTrue(isinstance(i, Weather))
            self.assertIsNotNone(i.get_date())
            self.assertIsNotNone(i.get_details())
            self.assertIsNotNone(i.get_temp())
            self.assertIsNotNone(i.get_weather())
            self.assertIsNotNone(i.get_description())
            self.assertTrue(isinstance(str(i), str))

        # test the search invalid case
        test2 = get_weather("q")
        self.assertEqual(1, test2)


if __name__ == '__main__':
    unittest.main()
