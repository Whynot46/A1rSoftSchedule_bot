import sqlite3


conn = sqlite3.connect('./db/events.db')
cursor = conn.cursor()


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


conn.commit()
conn.close()