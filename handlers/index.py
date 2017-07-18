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
        queryParam1 = self.get_argument("routeName").encode('utf-8')
        queryParam2 = self.get_argument("routeID").encode('utf-8')
        queryParam3 = self.get_argument("routeProvider").encode('utf-8')
        queryParam4 = self.get_argument("routeShort").encode('utf-8')
        response = self.executeRouteQuery(queryParam1, queryParam2, queryParam3, queryParam4)
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

    def executeRouteQuery(self, queryParam1, queryParam2, queryParam3, queryParam4):
        dbPath = "db.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()

        try:
            cursorobj.execute("""
                SELECT route_id, agency_name, route_short_name, route_long_name, agency_url
                FROM routes
                INNER JOIN agency ON routes.agency_id = agency.agency_id
                WHERE route_long_name LIKE '%{0}%' AND route_id LIKE '%{1}%' AND agency_name LIKE '%{2}%' AND route_short_name LIKE '%{3}%'
                ORDER BY route_id
            """.format(queryParam1, queryParam2, queryParam3, queryParam4))
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
            raise

        connection.close()
        return result


class Stops(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/stops.html",
            title="GTFS Viewer",
            stops=dao.stops()
        )

    def post(self):
        queryParam1 = self.get_argument("stopID").encode('utf-8')
        queryParam2 = self.get_argument("stopName").encode('utf-8')
        response = self.executeStopQuery(queryParam1, queryParam2)
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

    def executeStopQuery(self, queryParam1, queryParam2):
        dbPath = "db.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()

        try:
            cursorobj.execute("""
                SELECT stop_id, stop_name, stop_lat, stop_lon
                FROM stops
                WHERE stop_id LIKE '%{0}%' AND stop_name LIKE '%{1}%'
                ORDER BY stop_id
            """.format(queryParam1, queryParam2))
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
                raise

        connection.close()
        return result


class Trips(tornado.web.RequestHandler):
    def post(self):
        queryParam = self.get_argument("routeID").encode('utf-8')
        response = self.executeTripQuery(queryParam)
        data = []
        for a, b in response:
            item = {}
            item['trip_id'] = a
            item['trip_headsign'] = b
            data.append(item)

        self.write(json.dumps(data))

    def executeTripQuery(self, queryParam):
        dbPath = "db.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()

        try:
            cursorobj.execute("""
                SELECT trips.trip_id, trips.trip_headsign
                FROM trips
                INNER JOIN routes ON routes.route_id = trips.route_id
                WHERE trips.route_id IS '{0}'
            """.format(queryParam))
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
            raise

        connection.close()
        return result


class TripStops(tornado.web.RequestHandler):
    def post(self):
        queryParam = self.get_argument("tripID").encode('utf-8')
        response = self.executeTripStopsQuery(queryParam)
        data = []
        for a, b, c, d, e, f, g, h, i in response:
            item = {}
            item['stop_id'] = a
            item['stop_name'] = b
            item['stop_lat'] = c
            item['stop_lon'] = d
            item['stop_sequence'] = e
            item['shape_dist_traveled'] = f
            item['trip_id'] = g
            item['arrival_time'] = h
            item['departure_time'] = i
            data.append(item)

        self.write(json.dumps(data))

    def executeTripStopsQuery(self, queryParam):
        dbPath = "db.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()

        try:
            cursorobj.execute("""
                SELECT stops.stop_id, stops.stop_name, stops.stop_lat, stops.stop_lon, stop_times.stop_sequence, stop_times.shape_dist_traveled, stop_times.trip_id, stop_times.arrival_time, stop_times.departure_time
                FROM stop_times
                INNER JOIN stops ON stop_times.stop_id = stops.stop_id
                WHERE stop_times.trip_id IS '{0}'
            """.format(queryParam))
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
            raise

        connection.close()
        return result


class Dates(tornado.web.RequestHandler):
    def post(self):
        queryParam = self.get_argument("tripID").encode('utf-8')
        response = self.executeDateQuery(queryParam)
        data = []
        for a, b in response:
            item = {}
            item['trip_id'] = a
            item['date'] = b
            data.append(item)

        self.write(json.dumps(data))

    def executeDateQuery(self, queryParam):
        dbPath = "db.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()

        try:
            cursorobj.execute("""
                SELECT trips.trip_id, calendar_dates.date
                FROM trips
                INNER JOIN calendar_dates ON trips.service_id = calendar_dates.service_id
                WHERE trips.trip_id IS '{0}'
                ORDER BY calendar_dates.date
            """.format(queryParam))
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
                raise

        connection.close()
        return result


class StopTimes(tornado.web.RequestHandler):
    def post(self):
        queryParam1 = self.get_argument("tripID").encode('utf-8')
        queryParam2 = self.get_argument("stopID").encode('utf-8')
        response = self.executeStopTimesQuery(queryParam1, queryParam2)
        data = []
        for a, b, c in response:
            item = {}
            item['stop_id'] = a
            item['arrival_time'] = b
            item['departure_time'] = c
            data.append(item)

        self.write(json.dumps(data))

    def executeStopTimesQuery(self, queryParam1, queryParam2):
        dbPath = "db.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()

        try:
            cursorobj.execute("""
                SELECT stop_times.stop_id, stop_times.arrival_time, stop_times.departure_time
                FROM stop_times
                WHERE stop_times.trip_id IS '{0}' AND stop_times.stop_id IS '{1}'
                ORDER BY stop_times.stop_id
            """.format(queryParam1, queryParam2))
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
                raise

        connection.close()
        return result

# def load_gtfs():
#     # print(dao)
#     dao.load_gtfs("matka_gtfs.zip")
