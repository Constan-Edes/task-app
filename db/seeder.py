import sqlite3 as sql
from db_manager import create_db, create_table
from datetime import datetime

# for run the app in other pc pls execute this code

DB_PATH = "db/tasks.db"

table = """CREATE TABLE IF NOT EXISTS tasks 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            date TEXT, 
            status TEXT)"""

def addValues():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    data = [
        ('Make the App', '2022-01-1', 'Completada'),
        ('Buy coffee', '2000-06-11', 'Completada'),
        ('Watch Anime', '2020-02-22', 'Pendiente'),
        ('Play Games', '2022-04-2', 'Pendiente')
    ]
    cursor.executemany("INSERT INTO tasks VALUES (NULL, ?, ?, ?)", data)
    conn.commit()
    conn.close() 


if __name__ == "__main__":
    create_db(DB_PATH)
    create_table(DB_PATH, table)
    addValues()
    