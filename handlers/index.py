import tornado.web
import tornado.escape
from tornado.escape import json_decode

import json

from db import createDBConnection, executeQuery

db_name = "gtfs" # "db.sqlite"

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
            title="GTFS Viewer"
        )

    def post(self):
        response = self.executeRouteQuery(
            self.get_argument("routeID"),
            self.get_argument("routeShort")
        )

        data = []
        for a, b, c, d, e in response:
            item = {}
            item['route_id'] = a
            item['agency_name'] = b
            item['route_short_name'] = c
            item['route_long_name'] = d
            item['agency_url'] = e
            data.append(item)

        self.write(json.dumps(data))

    def executeRouteQuery(self, queryParam1, queryParam2):
        connection = createDBConnection(db_name)

        statement = None

        if len(queryParam1) > 0 and len(queryParam2) > 0:
            statement = """
                SELECT route_id, agency_name, route_short_name, route_long_name, agency_url
                FROM routes, agency
                WHERE routes.agency_id = agency.agency_id
                    AND route_id LIKE '%s'
                    AND route_short_name LIKE '%s'
                ORDER BY route_id
            """ % (queryParam1, queryParam2)

        if len(queryParam1) > 0 and len(queryParam2) == 0:
            statement = """
                SELECT route_id, agency_name, route_short_name, route_long_name, agency_url
                FROM routes, agency
                WHERE routes.agency_id = agency.agency_id
                    AND route_id LIKE '%s'
                ORDER BY route_id
            """ % (queryParam1)

        if len(queryParam1) == 0 and len(queryParam2) > 0:
            statement = """
                SELECT route_id, agency_name, route_short_name, route_long_name, agency_url
                FROM routes, agency
                WHERE routes.agency_id = agency.agency_id
                    AND route_short_name LIKE '%s'
                ORDER BY route_id
            """ % (queryParam2)

        print(statement)
        return executeQuery(connection, statement)



class Stops(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/stops.html",
            title="GTFS Viewer"
        )

    def post(self):
        response = self.executeStopQuery(
            self.get_argument("stopID"),
            self.get_argument("stopName")
        )

        data = []
        for a, b, c, d in response:
            item = {}
            item['stop_id'] = a
            item['stop_name'] = b
            item['stop_lat'] = str(c)
            item['stop_lon'] = str(d)
            data.append(item)

        self.write(json.dumps(data))

    def executeStopQuery(self, queryParam1, queryParam2):
        connection = createDBConnection(db_name)
        statement = """
            SELECT stop_id, stop_name, stop_lat, stop_lon
            FROM stops
            WHERE stop_id LIKE '%s'
                OR stop_name LIKE '%s'
            ORDER BY stop_id
        """ % (queryParam1, queryParam2.lower())
        return executeQuery(connection, statement)



class StopRoutes(tornado.web.RequestHandler):
    def post(self):
        stopRoutes = self.executeStopRouteQuery(self.get_argument("stopID"))

        stoproute_data = []
        for a, b, c in stopRoutes:
            item = {}
            item['route_id'] = a
            item['route_short_name'] = b
            item['route_long_name'] = c
            stoproute_data.append(item)

        self.write(json.dumps(stoproute_data))

    def executeStopRouteQuery(self, queryParam):
        connection = createDBConnection(db_name)
        statement = """
            SELECT DISTINCT trips.route_id, route_short_name, route_long_name
            FROM stop_times, trips, routes
            WHERE trips.trip_id = stop_times.trip_id
                AND trips.route_id = routes.route_id
                AND stop_id = '%s'
            ORDER BY trips.route_id
        """ % (queryParam)
        return executeQuery(connection, statement)



class StopTrips(tornado.web.RequestHandler):
    def post(self):
        trips = self.executeTripQuery(
            self.get_argument("routeID"),
            self.get_argument("stopID")
        )

        trip_data = []
        for a, b, c, d, e in trips:
            item = {}
            item['trip_id'] = a
            item['trip_headsign'] = b
            item['service_id'] = c
            item['arrival_time'] = str(d)
            item['departure_time'] = str(e)
            trip_data.append(item)

        self.write(json.dumps(trip_data))

    def executeTripQuery(self, queryParam1, queryParam2):
        connection = createDBConnection(db_name)
        statement = """
            SELECT trips.trip_id, trip_headsign, service_id, arrival_time, departure_time
            FROM trips, stop_times
            WHERE trips.trip_id = stop_times.trip_id AND
                (route_id = '%s' OR stop_id = '%s')
            ORDER BY arrival_time, departure_time
        """ % (queryParam1, queryParam2)
        return executeQuery(connection, statement)



class Trips(tornado.web.RequestHandler):
    def post(self):
        trips = self.executeTripQuery(self.get_argument("routeID"))

        trip_data = []
        for a, b, c in trips:
            item = {}
            item['trip_id'] = a
            item['trip_headsign'] = b
            item['service_id'] = c
            trip_data.append(item)

        self.write(json.dumps(trip_data))

    def executeTripQuery(self, queryParam):
        connection = createDBConnection(db_name)
        statement = """
            SELECT trip_id, trip_headsign, service_id
            FROM trips
            WHERE route_id = '%s'
        """ % (queryParam)
        return executeQuery(connection, statement)



class TripStops(tornado.web.RequestHandler):
    def post(self):
        response = self.executeTripStopsQuery(self.get_argument("tripID"))

        data = []
        for a, b, c, d, e, f, g, h in response:
            item = {}
            item['stop_id'] = a
            item['stop_name'] = b
            item['stop_lat'] = str(c)
            item['stop_lon'] = str(d)
            item['stop_sequence'] = e
            item['trip_id'] = f
            item['arrival_time'] = str(g)
            item['departure_time'] = str(h)
            data.append(item)

        self.write(json.dumps(data))

    def executeTripStopsQuery(self, queryParam):
        connection = createDBConnection(db_name)
        statement = """
            SELECT stops.stop_id, stops.stop_name, stops.stop_lat, stops.stop_lon, stop_times.stop_sequence, stop_times.trip_id, stop_times.arrival_time, stop_times.departure_time
            FROM stop_times, stops
            WHERE stop_times.stop_id = stops.stop_id
                AND stop_times.trip_id = '%s'
        """ % (queryParam)
        return executeQuery(connection, statement)



class TripDates(tornado.web.RequestHandler):
    def post(self):
        response = self.executeDateQuery(self.get_argument("tripID"))

        data = []
        for a, b in response:
            item = {}
            item['trip_id'] = a
            item['date'] = str(b)
            data.append(item)

        self.write(json.dumps(data))

    def executeDateQuery(self, queryParam):
        connection = createDBConnection(db_name)
        statement = """
            SELECT trips.trip_id, universal_calendar.date
            FROM trips, universal_calendar
            WHERE trips.service_id = universal_calendar.service_id
                AND trips.trip_id = '%s'
            ORDER BY universal_calendar.date
        """ % (queryParam)
        return executeQuery(connection, statement)
