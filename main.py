import os

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
            url(r"/dates", handlers.index.Dates),
            url(r"/stopTimes", handlers.index.StopTimes),
            url(r"/stopRoutes", handlers.index.StopRoutes),
            url(r"/stopPassingTimes", handlers.index.StopPassingTimes)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, routes, **settings)

def main():
    def fn():
        print "Reloading..."

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(5000)
    print("Listening on port: 5000")

    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
