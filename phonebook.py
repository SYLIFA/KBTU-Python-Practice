import sqlite3
import csv

def create_db():
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS contacts (name TEXT, phone TEXT UNIQUE)')
    conn.commit()
    conn.close()

def upload_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        conn = sqlite3.connect('phonebook.db')
        cursor = conn.cursor()
        cursor.executemany('INSERT OR REPLACE INTO contacts VALUES (?, ?)', reader)
        conn.commit()
        conn.close()

def search_contact(pattern):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    # Поиск по части имени или номера
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f'%{pattern}%', f'%{pattern}%'))
    results = cursor.fetchall()
    conn.close()
    return results

def delete_contact(name):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# Пример пагинации
def get_paged_contacts(limit, offset):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts LIMIT ? OFFSET ?", (limit, offset))
    return cursor.fetchall()