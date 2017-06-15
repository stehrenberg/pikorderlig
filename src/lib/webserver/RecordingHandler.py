import tornado.web
import json

class RecordingHandler(tornado.web.RequestHandler):
    def initialize(self, webserver_queue, manager_queue):
        self._webserver_queue = webserver_queue
        self._manager_queue = manager_queue

    def get(self, action):
        if not action in dir(self):
            self.set_status(404)
            self.write('404: Not Found')
        else:
            self.set_status(200)
            self.set_header('Content-Type', 'Application/json')
            self.set_header('Access-Control-Allow-Origin', '*')
            method_to_call = getattr(self, action)
            content = method_to_call()
            self.write(json.dumps(content))

    def start(self):
        self._manager_queue.put('recording:start')
        return {"status": "OK"}

    def stop(self):
        self._manager_queue.put('recording:stop')
        return {"status": "OK"}