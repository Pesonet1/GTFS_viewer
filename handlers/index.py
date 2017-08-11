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
            self.get_argument("routeName").encode('utf-8'),
            self.get_argument("routeID").encode('utf-8'),
            self.get_argument("routeProvider").encode('utf-8'),
            self.get_argument("routeShort").encode('utf-8')
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

    def executeRouteQuery(self, queryParam1, queryParam2, queryParam3, queryParam4):
        connection = createDBConnection(db_name)
        statement = """
            SELECT route_id, agency_name, route_short_name, route_long_name, agency_url
            FROM routes, agency
            WHERE routes.agency_id = agency.agency_id
                AND lower(route_long_name) LIKE '%{0}%'
                AND route_id LIKE '%{1}%'
                AND lower(agency_name) LIKE '%{2}%'
                AND lower(route_short_name) LIKE '%{3}%'
            ORDER BY route_id
        """
        return executeQuery(connection, statement, queryParam1, queryParam2, queryParam3, queryParam4)



class Stops(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/stops.html",
            title="GTFS Viewer"
        )

    def post(self):
        response = self.executeStopQuery(
            self.get_argument("stopID").encode('utf-8'),
            self.get_argument("stopName").encode('utf-8')
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
            WHERE stop_id LIKE '%{0}%'
                AND lower(stop_name) LIKE '%{1}%'
            ORDER BY stop_id
        """
        return executeQuery(connection, statement, queryParam1, queryParam2)



class StopRoutes(tornado.web.RequestHandler):
    def post(self):
        stopRoutes = self.executeStopRouteQuery(self.get_argument("stopID").encode('utf-8'))

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
                AND stop_id = '{0}'
            ORDER BY trips.route_id
        """
        return executeQuery(connection, statement, queryParam)



class StopPassingTimes(tornado.web.RequestHandler):
    def post(self):
        passTimes = self.executeStopPasstimeQuery(self.get_argument("stopID").encode('utf-8'))

        passtimes_data = []
        for a, b, c, d in passTimes:
            item = {}
            item['stop_id'] = a
            item['trip_id'] = b
            item['arrival_time'] = str(c)
            item['departure_time'] = str(d)
            passtimes_data.append(item)

        self.write(json.dumps(passtimes_data))

    def executeStopPasstimeQuery(self, queryParam):
        connection = createDBConnection(db_name)
        statement = """
            SELECT stop_id, trip_id, arrival_time, departure_time
            FROM stop_times
            WHERE stop_id = '{0}'
        """
        return executeQuery(connection, statement, queryParam)



class Trips(tornado.web.RequestHandler):
    def post(self):
        trips = self.executeTripQuery(self.get_argument("routeID").encode('utf-8'))

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
            WHERE route_id = '{0}'
        """
        return executeQuery(connection, statement, queryParam)



class TripStops(tornado.web.RequestHandler):
    def post(self):
        response = self.executeTripStopsQuery(self.get_argument("tripID").encode('utf-8'))

        data = []
        print response
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
                AND stop_times.trip_id = '{0}'
        """
        return executeQuery(connection, statement, queryParam)



class TripDates(tornado.web.RequestHandler):
    def post(self):
        response = self.executeDateQuery(self.get_argument("tripID").encode('utf-8'))

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
                AND trips.trip_id = '{0}'
            ORDER BY universal_calendar.date
        """
        return executeQuery(connection, statement, queryParam)



class StopTimes(tornado.web.RequestHandler):
    def post(self):
        response = self.executeStopTimesQuery(
            self.get_argument("tripID").encode('utf-8'),
            self.get_argument("stopID").encode('utf-8')
        )

        data = []
        for a, b, c in response:
            item = {}
            item['stop_id'] = a
            item['arrival_time'] = str(b)
            item['departure_time'] = str(c)
            data.append(item)

        self.write(json.dumps(data))

    def executeStopTimesQuery(self, queryParam1, queryParam2):
        connection = createDBConnection(db_name)
        statement = """
            SELECT stop_id, arrival_time, departure_time
            FROM stop_times
            WHERE trip_id = '{0}'
                AND stop_id = '{1}'
            ORDER BY stop_id
        """
        return executeQuery(connection, statement, queryParam1, queryParam2)
