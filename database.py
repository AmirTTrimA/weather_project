#database.py
import json
import sqlite3
from contextlib import closing

class WeatherDatabase:
    def __init__(self, db_name='weather_data.db'):
        self.db_name = db_name
        self.conn = self.connect()
        self.create_tables()

    def create_tables(self):
        with closing(self.connect()) as conn:
            with conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        temperature REAL NOT NULL,
                        feels_like REAL NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                ''')
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS stats (
                        total_requests INTEGER DEFAULT 0,
                        successful_requests INTEGER DEFAULT 0,
                        unsuccessful_requests INTEGER DEFAULT 0,
                        city_request_counts TEXT DEFAULT '{}'
                    )
                ''')
                # Initialize stats if the table is empty
                conn.execute('INSERT INTO stats (total_requests, successful_requests, unsuccessful_requests) VALUES (0, 0, 0)')

    def connect(self):
        return sqlite3.connect(self.db_name)
    
    def close(self):
        if self.conn:
            self.conn.close()  # Close the database connection

    def save_weather_data(self, city, temperature, feels_like, timestamp):
        with closing(self.connect()) as conn:
            with conn:
                conn.execute('''
                    INSERT INTO weather (city, temperature, feels_like, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (city, temperature, feels_like, timestamp))
                # self.connection.commit()


    def update_request_stats(self, success, city):
        with closing(self.connect()) as conn:
            with conn:
                # Update total requests
                conn.execute('UPDATE stats SET total_requests = total_requests + 1')

                # Update successful or unsuccessful requests
                if success:
                    conn.execute('UPDATE stats SET successful_requests = successful_requests + 1')
                else:
                    conn.execute('UPDATE stats SET unsuccessful_requests = unsuccessful_requests + 1')

                # Update city request counts
                cursor = conn.execute('SELECT city_request_counts FROM stats')
                row = cursor.fetchone()

                # Initialize city_request_counts if it doesn't exist
                if row is None or row[0] is None:
                    city_counts = {}
                else:
                    city_counts = json.loads(row[0])  # Use json.loads instead of eval

                # Increment the request count for the city
                city_counts[city] = city_counts.get(city, 0) + 1

                # Update the city_request_counts in the database
                conn.execute('UPDATE stats SET city_request_counts = ?',
                            (json.dumps(city_counts),))  # Use json.dumps to store

    def fetch_weather_data(self):
        with closing(self.connect()) as conn: 
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM weather')
            return cursor.fetchall()

    def fetch_stats(self):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM stats')
            rows = cursor.fetchall()

            stats_list = []
            for row in rows:
                if len(row) >= 4:  # Ensure there are at least 4 elements
                    total_requests = row[0]  # Assuming this is the ID
                    successful_requests = row[1]
                    unsuccessful_requests = row[2]
                    city_request_counts = json.loads(row[3]) if row[3] else {}  # Column 4

                    stats_dict = {
                        "total_requests": total_requests,
                        "successful_requests": successful_requests,
                        "unsuccessful_requests": unsuccessful_requests,
                        "city_request_counts": city_request_counts
                    }
                    stats_list.append(stats_dict)
                else:
                    print(f"Row length {len(row)} is less than expected. Row: {row}")

            return stats_list

    def delete_all_stats(self):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM stats')  # Deletes all records
            conn.commit()

    def delete_all_weather(self):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM weather')  # Deletes all records
            conn.commit()
