import tornado.web

class RecordingHandler(tornado.web.RequestHandler):
    def initialize(self, webserver_queue):
        self._queue = webserver_queue

    def get(self, action):
        print('Webserver action is ', action)
        if not action in dir(self):
            self.set_status(404)
        else:
            self.set_status(200)
            method_to_call = getattr(self, action)
            method_to_call()

    def start(self):
        self._queue.put('recording:start')

    def stop(self):
        self._queue.put('recording:stop')