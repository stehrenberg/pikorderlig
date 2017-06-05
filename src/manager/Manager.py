from multiprocessing import Process
import time

class Manager(Process):

    _recorder = None
    _recorder_queue = None
    _webserver = None
    _webserver_queue = None

    def __init__(self, manager_queue):
        Process.__init__(self)
        self._manager_queue = manager_queue
        self._action_mappings = {}

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

    def add_action_mappings(self, action_handler):
        action_mappings = action_handler.get_action_mappings()
        for action, method in action_mappings.items():
            self._action_mappings[action] = method

    def _handle_action(self, action):
        print("*** Handling queue action: ", action)
        method_to_call = self._action_mappings.get(action, self._action_not_found)

        method_to_call()


    def _action_not_found(self):
        raise LookupError

