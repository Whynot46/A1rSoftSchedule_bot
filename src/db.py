import sqlite3


DB_PATH = "./db/data.db"


def add_new_event(event_name, datetime, district, subject, address, location_info, game_type, event_info, group_link):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO events (event_name, datetime, district, subject, address, location_info, game_type, event_info, group_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_name, datetime, district, subject, address, location_info, game_type, event_info, group_link))
    connection.commit()
    

def get_names_by_subject(subject):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT event_name FROM events WHERE subject =?', (subject,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_data(event_name, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'SELECT {data} FROM events WHERE event_name = ?', (event_name,))
    rows = cursor.fetchall()
    conn.close()
    try:
        return rows[0][0]
    except: return None


def delete_old_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE datetime < datetime("now")')
    conn.commit()

    