from multiprocessing import Process
import time

class Manager(Process):

    def __init__(self, manager_queue):
        Process.__init__(self)
        self._manager_queue = manager_queue

    def run(self):
        print("*** Manager starting up")
        # iteriert durch msg queue und arbeitet Auftraege ab

        while True:
            action = self._manager_queue.get()
            self._handle_action(action)
            time.sleep(0.2)

    def set_webserver(self, webserver, webserver_queue):
        self._webserver = webserver
        self._webserver_queue = webserver_queue

    def set_recorder(self, recorder, recorder_queue):
        self._recorder = recorder
        self._recorder_queue = recorder_queue

    def _handle_action(self, action):
        print("*** Handling queue action: ", action)

        action_mapper = {
            'recording:start' : self._recorder.start_recording,
            'recording:stop' : self._recorder.stop_recording
        }

        method_to_call = action_mapper.get(action, self._action_not_found)
        method_to_call()

    def _action_not_found(self):
        raise LookupError

