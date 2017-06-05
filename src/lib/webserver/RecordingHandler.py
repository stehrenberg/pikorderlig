import tornado.web

class RecordingHandler(tornado.web.RequestHandler):
    def get(self, action):
        print('Webserver action is ', action)