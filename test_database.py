import unittest
import os
from datetime import datetime

from database import WeatherDatabase

class TestWeatherDatabase(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test_weather_data.db'
        self.db = WeatherDatabase(db_name=self.db_name)

    def tearDown(self):
        self.db.close()  # Now this will work correctly
        os.remove(self.db_name)  # Remove the database file


    def test_save_and_fetch_weather_data(self):
        # Example timestamp from OpenWeatherMap
        timestamp = datetime.now().isoformat()  # Use current time as a timestamp

        # Save some weather data
        self.db.save_weather_data('London', 15.0, 14.0, timestamp)
        self.db.save_weather_data('New York', 20.0, 19.0, timestamp)

        # Fetch the weather data
        data = self.db.fetch_weather_data()

        # Check that the data is saved correctly
        self.assertEqual(len(data), 2)  # We should have 2 records
        self.assertIn(('London', 15.0, 14.0, timestamp), [(row[1], row[2], row[3], row[4]) for row in data])  # Check London data
        self.assertIn(('New York', 20.0, 19.0, timestamp), [(row[1], row[2], row[3], row[4]) for row in data])  # Check New York data

    def test_update_request_stats(self):
        # Initialize stats
        self.db.update_request_stats(True, 'London')  # Simulate a successful request
        self.db.update_request_stats(False, 'London')  # Simulate an unsuccessful request

        # Fetch the updated stats
        rows = self.db.fetch_stats()  # Now returns a list of rows
        row = rows[0]  # Get the first (and likely only) row

        # Check the counts
        self.assertEqual(row[1], 1)  # successful_requests
        self.assertEqual(row[2], 1)  # unsuccessful_requests
        city_counts = eval(row[3])  # Convert back to dict
        self.assertEqual(city_counts['London'], 2)  # Total requests for London should be 2

if __name__ == '__main__':
    unittest.main()
