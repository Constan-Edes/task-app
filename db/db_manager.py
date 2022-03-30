import sqlite3 as sql

def create_db(name):
    conn = sql.connect(name) # create SQLite database
    conn.commit() # commit changes
    conn.close() # close connection


def create_table(db_name, query):
    conn = sql.connect(db_name)
    c = conn.cursor() # create a cursor 
    c.execute(query) # execute query
    conn.close()

def sql_query(db_name, query):
    conn = sql.connect(db_name) 
    c = conn.cursor() 
    c.execute(query) # execute query
    conn.commit() 
    conn.close()


if __name__ == "__main__":
   pass
