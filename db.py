import sqlite3

# Create a connection to the database (or create it if it doesn't exist)
conn = sqlite3.connect(r'D:\MKT\MaktabHW\HW16\weather_project\weather_data.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS stats;')