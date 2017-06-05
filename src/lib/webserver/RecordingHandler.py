import tornado.web
import json

class RecordingHandler(tornado.web.RequestHandler):
    def initialize(self, webserver_queue):
        self._queue = webserver_queue

    def get(self, action):
        if not action in dir(self):
            self.set_status(404)
        else:
            self.set_status(200)
            self.set_header('Content-Type', 'Application/json')
            method_to_call = getattr(self, action)
            content = method_to_call()
            self.write(json.dumps(content))

    def start(self):
        self._queue.put('recording:start')
        return {"status": "OK"}

    def stop(self):
        self._queue.put('recording:stop')
        return {"status": "OK"}