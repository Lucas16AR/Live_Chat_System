import sqlite3
import time

def display_messages():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    last_displayed_id = None

    while True:
        if last_displayed_id is None:
            cursor.execute("SELECT id, username, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 1")
        else:
            cursor.execute("SELECT id, username, message, timestamp FROM messages WHERE id > ? ORDER BY timestamp ASC", (last_displayed_id,))
        
        rows = cursor.fetchall()

        for row in rows:
            print(f'[{row[3]}] {row[1]}: {row[2]}')
            last_displayed_id = row[0]

        time.sleep(1)

display_messages()