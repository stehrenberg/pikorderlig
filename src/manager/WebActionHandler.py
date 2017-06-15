class WebActionHandler:

    def __init__(self, recorder, webserver_queue):
        self._recorder = recorder
        self._webserver_queue = webserver_queue

        self._action_mappings = {
            'web:recording:status': self._get_recorder_status
        }

    def _get_recorder_status(self):
        status = self._recorder.get_status()
        self._webserver_queue.put(status)

    def get_action_mappings(self):
        return self._action_mappings
