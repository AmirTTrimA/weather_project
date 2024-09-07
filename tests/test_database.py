import unittest
import os
from datetime import datetime

from database import WeatherDatabase

class TestWeatherDatabase(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test_weather_data.db'
        self.db = WeatherDatabase(db_name=self.db_name)

    def tearDown(self):
        self.db.close()
        os.remove(self.db_name)


    def test_save_and_fetch_weather_data(self):
        timestamp = datetime.now().isoformat()

        self.db.save_weather_data('London', 15.0, 14.0, timestamp)
        self.db.save_weather_data('New York', 20.0, 19.0, timestamp)

        data = self.db.fetch_weather_data()

        self.assertEqual(len(data), 2)
        self.assertIn(('London', 15.0, 14.0, timestamp), [(row[1], row[2], row[3], row[4]) for row in data])
        self.assertIn(('New York', 20.0, 19.0, timestamp), [(row[1], row[2], row[3], row[4]) for row in data])

    def test_update_request_stats(self):
        self.db.update_request_stats(True, 'London')
        self.db.update_request_stats(False, 'London')

        rows = self.db.fetch_stats()
        row = rows[0]

        self.assertEqual(row[1], 1)
        self.assertEqual(row[2], 1)
        city_counts = eval(row[3])
        self.assertEqual(city_counts['London'], 2)

if __name__ == '__main__':
    unittest.main()
