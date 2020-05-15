import sqlite3
from sqlite3 import Error

import psycopg2
from psycopg2 import connect

def createDBConnection(db_file):
    try:
        if db_file == "gtfs":
            conn = connect(dbname="gtfs", user="postgres", host="localhost", password="postgres", connect_timeout=30)
        else:
            conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def executeQuery(connection, query):
    result = None

    try:
        cursorobj = connection.cursor()
        cursorobj.execute(query)
        result = cursorobj.fetchall()
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()
        raise e
    finally:
        connection.close()
        return result
