import http.client
import json
import urllib.parse
import socket
from datetime import datetime, timezone
import pytz

def convert_utc_to_local(utc_time, local_tz):
    local_time = utc_time.astimezone(local_tz)
    return local_time

def start_client():
    local_tz = pytz.timezone('Asia/Tehran')
    
    while True:
        city_name = input("Enter a city name: ")
        if city_name.lower() == 'exit':
            break
        
        encoded_city_name = urllib.parse.quote(city_name)

        conn = http.client.HTTPConnection("localhost", 8080, timeout=5)
        try:
            conn.request("GET", f"/weather/{encoded_city_name}")
            response = conn.getresponse()
            
            if response.status == 200:
                data = json.loads(response.read())
                city = data.get('city', 'Unknown city')
                temperature = data.get('temperature', 'N/A')
                feels_like = data.get('feels_like', 'N/A')
                timestamp = data.get('timestamp', None)

                if timestamp is not None:
                    if isinstance(timestamp, int):
                        utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    else:
                        utc_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

                    local_time = convert_utc_to_local(utc_time, local_tz)
                    timestamp_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    timestamp_str = 'N/A'

                print(f"City: {city},\nTemperature: {temperature}°C,\nFeels Like: {feels_like}°C,\nTimestamp: {timestamp_str}")
            else:
                print("Error:", response.read().decode())
        except (socket.timeout, http.client.RemoteDisconnected) as e:
            print("Request timed out or remote server closed the connection:", e)
        except Exception as e:
            print("An error has occurred", e)
        finally:
            conn.close()

if __name__ == "__main__":
    start_client()
