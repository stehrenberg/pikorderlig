class VisualizerActionHandler:
    def __init__(self, visualizer_queue):
        self._visualizer_queue = visualizer_queue
        self._action_mappings = {
            'recording:started': self._recording_started,
            'recording:heartbeat': self._recording_heartbeat,
            'recording:stopped': self._recording_stopped,
            'recording:volume': self._recording_volume
        }

    def get_action_mappings(self):
        return self._action_mappings

    def _recording_started(self):
        self._visualizer_queue.put('recording:started')

    def _recording_stopped(self):
        self._visualizer_queue.put('recording:stopped')

    def _recording_heartbeat(self):
        self._visualizer_queue.put('recording:heartbeat')

    def _recording_volume(self):
        self._visualizer_queue.put('recording:volume')