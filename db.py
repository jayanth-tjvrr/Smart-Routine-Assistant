import sqlite3
from datetime import datetime

def get_db():
    conn = sqlite3.connect('routine.db')
    return conn

def get_user():
    # For MVP, no real user system
    return {}

def save_user_action(user, item, result):
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS actions (timestamp TEXT, task TEXT, result TEXT)''')
    c.execute('INSERT INTO actions VALUES (?, ?, ?)', (datetime.now().isoformat(), item['task'], result))
    conn.commit()
    conn.close()

def get_actions_for_date(date):
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS actions (timestamp TEXT, task TEXT, result TEXT)''')
    # Fetch all actions for the given date (date is a datetime.date)
    date_str = date.strftime('%Y-%m-%d')
    c.execute('SELECT timestamp, task, result FROM actions WHERE timestamp LIKE ?', (f'{date_str}%',))
    rows = c.fetchall()
    conn.close()
    return rows
