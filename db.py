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

def executeQuery(*args):
    try:
        cursorobj = args[0].cursor()

        if len(args) == 3: # 1 queryParam
            cursorobj.execute(args[1].format(args[2]))
        elif len(args) == 4: # 2 queryParam
            cursorobj.execute(args[1].format(args[2], args[3]))
        elif len(args) == 5: # 3 queryParam
            cursorobj.execute(args[1].format(args[2], args[3], args[4]))
        elif len(args) == 6: # 4 queryParam
            cursorobj.execute(args[1].format(args[2], args[3], args[4], args[5]))

        result = cursorobj.fetchall()
        args[0].commit()
    except Exception as e:
        args[0].rollback()
        raise e
    finally:
        args[0].close()
        return result
