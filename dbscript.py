import sqlite3
import os


def create_database(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_hist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city VARCHAR(255) default NULL)
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")
    finally:
        conn.close()


def insert_history(db_name, city):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO search_hist (city) VALUES (?)', (city,))
    conn.commit()
    conn.close()


def query_history(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search_hist')
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_database(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)
    else:
        print(f"The database file {db_name} does not exist.")
