import sqlite3 as sql
from db_manager import create_db, create_table

# for run the app at the first time, please execute this code

DB_PATH = "db/tasks.db"

table = """CREATE TABLE IF NOT EXISTS tasks 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT UNIQUE, 
            date TEXT, 
            status BOOLEAN NOT NULL DEFAULT 0 CHECK (status IN (0, 1)));"""

def addValues():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    data = [
        ('Make the App', '2022-04-02', '1'),
        ('Watch YT', '2020-02-22', '0'),
        ('Drink coffee', '2001-06-11', '1'),
        ('Play Games', '2016-10-02', '0'),
    ]
    cursor.executemany("INSERT INTO tasks VALUES (NULL, ?, ?, ?)", data)
    conn.commit()
    conn.close() 


if __name__ == "__main__":
    create_db(DB_PATH)
    create_table(DB_PATH, table)
    addValues()
    