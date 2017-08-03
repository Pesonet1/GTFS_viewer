import tornado.web
import tornado.escape
from tornado.escape import json_decode

import json
import pprint
import csv
import os

from db import createDBConnection, executeQuery

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
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT route_id, agency_name, route_short_name, route_long_name, agency_url
            FROM routes, agency
            WHERE routes.agency_id = agency.agency_id AND route_long_name LIKE '%{0}%' AND route_id LIKE '%{1}%' AND agency_name LIKE '%{2}%' AND route_short_name LIKE '%{3}%'
            ORDER BY route_id, agency_name, route_short_name
        """
        return executeQuery(connection, statement, queryParam1, queryParam2, queryParam3, queryParam4)



class Stops(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "../templates/stops.html",
            title="GTFS Viewer"
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

        self.write(json.dumps(data))

    def executeStopQuery(self, queryParam1, queryParam2):
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT stop_id, stop_name, stop_lat, stop_lon
            FROM stops
            WHERE stop_id LIKE '%{0}%' AND stop_name LIKE '%{1}%'
            ORDER BY stop_id
        """
        return executeQuery(connection, statement, queryParam1, queryParam2)



class StopRoutes(tornado.web.RequestHandler):
    def post(self):
        queryParam1 = self.get_argument("stopID").encode('utf-8')
        stopRoutes = self.executeStopRouteQuery(queryParam1)

        stoproute_data = []
        for a, b, c in stopRoutes:
            item = {}
            item['route_id'] = a
            item['route_short_name'] = b
            item['route_long_name'] = c
            stoproute_data.append(item)

        self.write(json.dumps(stoproute_data))

    def executeStopRouteQuery(self, queryParam):
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT trips.route_id, route_short_name, route_long_name
            FROM stop_times, trips, routes
            WHERE trips.trip_id = stop_times.trip_id
                AND trips.route_id = routes.route_id
                AND stop_id IS '{0}'
            ORDER BY trips.route_id
        """
        return executeQuery(connection, statement, queryParam)



class StopPassingTimes(tornado.web.RequestHandler):
    def post(self):
        queryParam = self.get_argument("stopID").encode('utf-8')
        passTimes = self.executeStopPasstimeQuery(queryParam)

        passtimes_data = []
        for a, b, c in passTimes:
            item = {}
            item['stop_id'] = a
            item['arrival_time'] = b
            item['departure_time'] = c
            passtimes_data.append(item)

        self.write(json.dumps(passtimes_data))

    def executeStopPasstimeQuery(self, queryParam):
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT stop_id, arrival_time, departure_time
            FROM stop_times
            WHERE stop_id IS '{0}'
        """
        return executeQuery(connection, statement, queryParam)



class Trips(tornado.web.RequestHandler):
    def post(self):
        queryParam = self.get_argument("routeID").encode('utf-8')
        trips = self.executeTripQuery(queryParam)

        trip_data = []
        for a, b, c in trips:
            item = {}
            item['trip_id'] = a
            item['trip_headsign'] = b
            item['service_id'] = c
            trip_data.append(item)

        self.write(json.dumps(trip_data))

    def executeTripQuery(self, queryParam):
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT trip_id, trip_headsign, service_id
            FROM trips
            WHERE route_id IS '{0}'
        """
        return executeQuery(connection, statement, queryParam)

    def executeTripTimeQuery(self, queryParam):
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT arrival_time, departure_time
            FROM stop_times
            WHERE trip_id IS '{0}'
        """
        return executeQuery(connection, statement, queryParam)



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
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT stops.stop_id, stops.stop_name, stops.stop_lat, stops.stop_lon, stop_times.stop_sequence, stop_times.shape_dist_traveled, stop_times.trip_id, stop_times.arrival_time, stop_times.departure_time
            FROM stop_times, stops
            WHERE stop_times.stop_id = stops.stop_id AND stop_times.trip_id IS '{0}'
        """
        return executeQuery(connection, statement, queryParam)



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
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT trips.trip_id, calendar_dates.date
            FROM trips, calendar_dates
            WHERE trips.service_id = calendar_dates.service_id AND trips.trip_id IS '{0}'
            ORDER BY calendar_dates.date
        """
        return executeQuery(connection, statement, queryParam)



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
        connection = createDBConnection("db.sqlite")
        statement = """
            SELECT stop_times.stop_id, stop_times.arrival_time, stop_times.departure_time
            FROM stop_times
            WHERE stop_times.trip_id IS '{0}' AND stop_times.stop_id IS '{1}'
            ORDER BY stop_times.stop_id
        """
        return executeQuery(connection, statement, queryParam1, queryParam2)
