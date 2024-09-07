#test_get_city_weather.py
import unittest
from unittest.mock import patch, MagicMock
from weather_info.main.weather_server import WeatherHandler
import http.client
import json

class TestWeatherHandler(unittest.TestCase):

    @patch('http.client.HTTPSConnection')
    def test_handle_weather_request_success(self, mock_https_connection):
        # Mock the response from OpenWeatherMap
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "name": "TestCity",
            "main": {"temp": 25, "feels_like": 24},
            "dt": 1609459200
        }).encode('utf-8')
        mock_https_connection.return_value.getresponse.return_value = mock_response
        
        handler = WeatherHandler()
        handler.database = MagicMock()  # Mock the database
        
        # Call the method with a test city
        handler.handle_weather_request("TestCity")
        
        # Check that the database's save_weather_data was called correctly
        handler.database.save_weather_data.assert_called_once_with(
            "TestCity", 25, 24, "2021-01-01 00:00:00"  # Adjust the expected timestamp format
        )

    @patch('http.client.HTTPSConnection')
    def test_handle_weather_request_failure(self, mock_https_connection):
        # Mock a failure response
        mock_response = MagicMock()
        mock_response.status = 404
        mock_response.read.return_value = b'{"error": "city not found"}'
        mock_https_connection.return_value.getresponse.return_value = mock_response
        
        handler = WeatherHandler()
        handler.database = MagicMock()  # Mock the database
        
        # Call the method with a test city
        handler.handle_weather_request("UnknownCity")
        
        # Check that the database's update_request_stats was called with success=False
        handler.database.update_request_stats.assert_called_once_with(success=False, city="UnknownCity")

if __name__ == '__main__':
    unittest.main()
