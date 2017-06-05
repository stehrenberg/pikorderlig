import tornado.ioloop
import tornado.web
from multiprocessing import Process
from lib.webserver.RecordingHandler import RecordingHandler

class Rest(Process):
    def __init__(self, queue):
        self._queue = queue

        application = tornado.web.Application([
            (r'/recording/(.*)', RecordingHandler)
        ])

        application.listen(8080)
        print("*** Webserver running on port 8080")
        tornado.ioloop.IOLoop.current().start()