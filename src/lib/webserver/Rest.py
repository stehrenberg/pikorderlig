import tornado.ioloop
import tornado.web
from multiprocessing import Process
from lib.webserver.RecordingHandler import RecordingHandler

class Rest(Process):
    def __init__(self, queue):
        Process.__init__(self)
        self._queue = queue

    def run(self):
        application = tornado.web.Application([
            (r'/recording/(.*)', RecordingHandler, dict(webserver_queue=self._queue))
        ])

        application.listen(8080)
        print("*** Webserver running on port 8080")
        tornado.ioloop.IOLoop.current().start()