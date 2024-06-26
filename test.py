import unittest
from main.py import get_weather, display_forecast
from dbscript.py import create_database, query_history, insert_history, delete_database     # noqa


class TestFileName(unittest.TestCase):
    exit
    # def test_function1(self):
    #     self.assertEqual(function1(1), 0)

    # def test_function2(self):
    #     self.assertEqual(function2(2,1), 3)
    #     self.assertEqual(function2(2.1, 1.2), 3.3)


if __name__ == '__main__':
    unittest.main()
