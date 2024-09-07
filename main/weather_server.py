#weather_server.py
import http.server
import socketserver
import json
import http.client
import os
from urllib.parse import urlparse, urlencode, unquote
from datetime import datetime, timedelta
from collections import defaultdict
from datetime import timezone

from database import WeatherDatabase

PORT = 8080

class WeatherHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.database = WeatherDatabase()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/weather/'):
            city_name = parsed_path.path.split('/')[-1]
            self.handle_weather_request(city_name)
        elif parsed_path.path == '/stats':
            self.handle_stats_request()
        elif parsed_path.path == '/stats_page':
            self.handle_stats_page()
        elif self.path == '/weather_data':
            self.handle_weather_data_request()
        elif parsed_path.path == '/weather_client':
            self.handle_weather_client_page()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid endpoint."}')


    def handle_stats_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_file_path = os.path.join('..' ,'html', 'stats.html')
        
        try:
            with open(html_file_path, 'r') as file:
                self.wfile.write(file.read().encode())
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def handle_weather_client_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_file_path = os.path.join('..' ,'html', 'client.html')
        
        try:
            with open(html_file_path, 'r') as file:
                self.wfile.write(file.read().encode())
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def handle_weather_request(self, city_name):
        city_name = unquote(city_name)
        conn = http.client.HTTPSConnection("api.openweathermap.org")
        api_key = "77632be90a0d4e96abab859050b10d98" ## **YOUR_API_KEY Should be replaced with your Open Weather Map API**
        params = urlencode({'q': city_name, 'appid': api_key, 'units': 'metric'})
        
        conn.request("GET", f"/data/2.5/weather?{params}")
        response = conn.getresponse()
        response_data = response.read()
        
        if response.status == 200:
            weather_data = json.loads(response_data)
            timestamp = weather_data.get("dt")
            formatted_timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            
            response_dict = {
                "city": weather_data.get("name"),
                "temperature": weather_data["main"].get("temp"),
                "feels_like": weather_data["main"].get("feels_like"),
                "timestamp": formatted_timestamp
            }
            
            self.database.save_weather_data(
                response_dict["city"],
                response_dict["temperature"],
                response_dict["feels_like"],
                response_dict["timestamp"]
            )
            self.database.update_request_stats(success=True, city=city_name)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response_dict).encode())
        else:
            self.database.update_request_stats(success=False, city=city_name)
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "City not found."}')

    def handle_weather_data_request(self):
        data = self.database.fetch_weather_data()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def handle_stats_request(self):
        stats = self.database.fetch_stats()
        if stats:
            total_requests = stats[0]["total_requests"]
            successful_requests = stats[0]["successful_requests"]
            unsuccessful_requests = stats[0]["unsuccessful_requests"]
            city_request_counts = stats[0]["city_request_counts"]
        else:
            total_requests = 0
            successful_requests = 0
            unsuccessful_requests = 0
            city_request_counts = {}

        stats_response = {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "unsuccessful_requests": unsuccessful_requests,
            "city_request_counts": city_request_counts
        }

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(stats_response).encode())

with socketserver.TCPServer(("", PORT), WeatherHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
