import sqlite3
from sqlite3 import Error

import psycopg2
from psycopg2 import connect

# from gtfslib.dao import Dao
# dao = Dao("db.sqlite")

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

# db load url postgresql://postgres:postgres@localhost:5432/gtfs
# gtfsdb-load --database_url postgresql://postgres:postgres@localhost:5432/gtfs matka.zip

# This function can be used for loading GTFS data in zip form... By default its location needs to be in root folder
# def load_gtfs(GTFS_filename):
#     dao.load_gtfs(GTFS_filename)
#
# def createValluTable():
#     conn = createDBConnection("vallu.sqlite")
#     cur = conn.cursor()
#     cur.execute("CREATE TABLE vallu_vuorot (lu_viranro_myontaa, viranomaisnimi, lu_viranro_valvoo, viranomaisnimi_1, lu_voim_pvm, lu_lop_pvm, lu_tod_loppvm, lupasoptunnus, muokattu_pvm, liikharjnro, liikharj_nimi, reittinro_pysyva, reittinimi, ajosuunta, linjan_tunnus, reitti_voimaan_pvm, reitti_paattyy_pvm, reittia_muokattu_pvm, vuorotunniste_pysyva, vuoromerk, lahtoaika, perilla, kausi, vuorotyyppi, vuoro_lisatunniste, vuoro_voimaan_pvm, vuoro_paattyy_pvm, vuoroa_muokattu_pvm, kasitelty_koontikartassa, siirtyy_matka_fi, vuoron_url_interpoloitu);")
#
#     conn.commit()
#     conn.close()
#
# def insertValluCSVtoTable():
#     conn = createDBConnection("vallu.sqlite")
#     cur = conn.cursor()
#
#     reader = csv.reader(open('handlers/vallu_vuorot.csv', 'rb'), delimiter=';')
#     for row in reader:
#         to_db = [
#             unicode(row[0], 'utf-8'),
#             unicode(row[1], 'utf-8'),
#             unicode(row[2], 'utf-8'),
#             unicode(row[3], 'utf-8'),
#             unicode(row[4], 'utf-8'),
#             unicode(row[5], 'utf-8'),
#             unicode(row[6], 'utf-8'),
#             unicode(row[7], 'utf-8'),
#             unicode(row[8], 'utf-8'),
#             unicode(row[9], 'utf-8'),
#             unicode(row[10], 'utf-8'),
#             unicode(row[11], 'utf-8'),
#             unicode(row[12], 'utf-8'),
#             unicode(row[13], 'utf-8'),
#             unicode(row[14], 'utf-8'),
#             unicode(row[15], 'utf-8'),
#             unicode(row[16], 'utf-8'),
#             unicode(row[17], 'utf-8'),
#             unicode(row[18], 'utf-8'),
#             unicode(row[19], 'utf-8'),
#             unicode(row[20], 'utf-8'),
#             unicode(row[21], 'utf-8'),
#             unicode(row[22], 'utf-8'),
#             unicode(row[23], 'utf-8'),
#             unicode(row[24], 'utf-8'),
#             unicode(row[25], 'utf-8'),
#             unicode(row[26], 'utf-8'),
#             unicode(row[27], 'utf-8'),
#             unicode(row[28], 'utf-8'),
#             unicode(row[29], 'utf-8'),
#             unicode(row[30], 'utf-8')
#         ]
#         cur.execute("INSERT INTO vallu_vuorot (lu_viranro_myontaa, viranomaisnimi, lu_viranro_valvoo, viranomaisnimi_1, lu_voim_pvm, lu_lop_pvm, lu_tod_loppvm, lupasoptunnus, muokattu_pvm, liikharjnro, liikharj_nimi, reittinro_pysyva, reittinimi, ajosuunta, linjan_tunnus, reitti_voimaan_pvm, reitti_paattyy_pvm, reittia_muokattu_pvm, vuorotunniste_pysyva, vuoromerk, lahtoaika, perilla, kausi, vuorotyyppi, vuoro_lisatunniste, vuoro_voimaan_pvm, vuoro_paattyy_pvm, vuoroa_muokattu_pvm, kasitelty_koontikartassa, siirtyy_matka_fi, vuoron_url_interpoloitu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
#
#     conn.commit()
#     conn.close()
