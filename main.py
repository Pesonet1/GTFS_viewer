import os
import signal

import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.autoreload
from tornado.web import url

import handlers.index

class Application(tornado.web.Application):
    def __init__(self):
        routes = [
            url(r"/", handlers.index.IndexHandler),
            url(r"/routes", handlers.index.Routes),
            url(r"/stops", handlers.index.Stops),
            url(r"/trips", handlers.index.Trips),
            url(r"/tripStops", handlers.index.TripStops),
            url(r"/tripDates", handlers.index.TripDates),
            url(r"/stopTrips", handlers.index.StopTrips),
            url(r"/stopRoutes", handlers.index.StopRoutes)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, routes, **settings)

def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    print('Stopping http server')
    http_server.stop()
    io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.stop()
    print('Shutdown')

def main():
    def fn():
        print("Reloading...")

    global http_server

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(5005)
    print("Listening on port: 5005")

    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
