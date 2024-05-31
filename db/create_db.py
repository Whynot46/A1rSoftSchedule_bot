import sqlite3


conn = sqlite3.connect('./db/data.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS events''')
cursor.execute('''
    CREATE TABLE events (
        event_name TEXT,
        datetime TEXT,
        district TEXT,
        subject TEXT,
        address TEXT,
        location_info TEXT,
        game_type TEXT,
        event_info TEXT,
        group_link TEXT
    )
    ''')

cursor.execute('''
    CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    event_name TEXT
    )
    ''')


conn.commit()
conn.close()