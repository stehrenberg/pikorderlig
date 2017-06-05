import tornado.ioloop
import tornado.web
from multiprocessing import Process
from lib.webserver.RecordingHandler import RecordingHandler

class Rest(Process):
    def __init__(self, webserver_queue, manager_queue):
        Process.__init__(self)
        self._webserver_queue = webserver_queue
        self._manager_queue = manager_queue

    def run(self):
        print("*** Starting Webserver")
        application = tornado.web.Application([
            (r'/recording/(.*)',
             RecordingHandler,
             dict(
                 webserver_queue=self._webserver_queue,
                 manager_queue=self._manager_queue
             ))
        ])

        application.listen(8080)
        print("*** Webserver running on port 8080")
        tornado.ioloop.IOLoop.current().start()