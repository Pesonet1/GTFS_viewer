import tornado.web
import tornado.escape
from tornado.escape import json_decode

import json
import pprint
import sqlite3

from gtfslib.dao import Dao

dao = Dao("db.sqlite")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/index.html",
            title="GTFS Viewer",
        )

class Routes(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/routes.html",
            title="GTFS Viewer",
            routes=dao.routes()
        )

    def post(self):
        queryParam = self.get_argument("routeName").encode('utf-8')
        response = executeRouteQuery(queryParam)
        data = []
        for a, b, c, d, e in response:
            item = {}
            item['route_id'] = a
            item['agency_name'] = b
            item['route_short_name'] = c
            item['route_long_name'] = d
            item['agency_url'] = e
            data.append(item)
        # queryRoutes = json.dumps(data)
        # queryRoutes = json.loads(queryRoutes)

        self.write(json.dumps(data))

class Stops(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/stops.html",
            title="GTFS Viewer",
            stops=dao.stops()
        )

    def post(self):
        queryParam = self.get_argument("stopName").encode('utf-8')
        response = executeStopQuery(queryParam)
        data = []
        for a, b, c, d in response:
            item = {}
            item['stop_id'] = a
            item['stop_name'] = b
            item['stop_lat'] = c
            item['stop_lon'] = d
            data.append(item)
        # queryStops = json.dumps(data)
        # queryStops = json.loads(queryRoutes)

        self.write(json.dumps(data))

def excecuteFullRouteQuery(route):
    dbPath = "db.sqlite"
    connection = sqlite3.connect(dbPath)
    cursorobj = connection.cursor()

    try:
        cursorobj.execute("""SELECT routes.route_long_name
                                FROM routes
                                INNER JOIN trips
                                    ON routes.route_id = trips.route_id
                                INNER JOIN stop_times
                                    ON trips.trip_id = stop_times.trip_id
                                INNER JOIN stops
                                    ON stop_times.stop_id = stops.stop_id
                                WHERE routes.route_long_name LIKE '%{0}%'""".format(route))
        result = cursorobj.fetchall()
        connection.commit()
    except Exception:
        raise

    connection.close()
    return result

def executeRouteQuery(queryParam):
    dbPath = "db.sqlite"
    connection = sqlite3.connect(dbPath)
    cursorobj = connection.cursor()

    # combine agency_id with the agency table to fetch the real names

    try:
        cursorobj.execute("""SELECT route_id, agency_name, route_short_name, route_long_name, agency_url FROM routes INNER JOIN agency ON routes.agency_id = agency.agency_id WHERE route_long_name LIKE '%{0}%'""".format(queryParam))
        result = cursorobj.fetchall()
        connection.commit()
    except Exception:
            raise

    connection.close()
    return result

def executeStopQuery(queryParam):
    dbPath = "db.sqlite"
    connection = sqlite3.connect(dbPath)
    cursorobj = connection.cursor()

    try:
        cursorobj.execute("""SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops WHERE stop_name LIKE '%{0}%'""".format(queryParam))
        result = cursorobj.fetchall()
        connection.commit()
    except Exception:
            raise

    connection.close()
    return result

# def load_gtfs():
#     # print(dao)
#     dao.load_gtfs("matka_gtfs.zip")
