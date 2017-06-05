from multiprocessing import Process
import time

class Manager(Process):

    def __init__(self, manager_queue):
        Process.__init__(self)
        self._manager_queue = manager_queue

    def run(self):
        print("*** Manager starting up")
        # spawned Prozesse für Webserver, Recorder, LEDs
        # spawned queues für einzelne prozesse
        # iteriert durch msg queue und arbeitet Auftraege ab

        while True:
            webserver_action = self._webserver_queue.get()
            self._handle_webserver_action(webserver_action)
            time.sleep(0.5)

    def set_webserver(self, webserver, webserver_queue):
        self._webserver = webserver
        self._webserver_queue = webserver_queue

    def set_recorder(self, recorder, recorder_queue):
        self._recorder = recorder
        self._recorder_queue = recorder_queue

    def _handle_webserver_action(self, action):
        print("*** Handling webserver queue action ", action)
        if action == 'recording:start':
            self._recorder.start_recording()

        elif action == 'recording:stop':
            self._recorder.stop_recording()