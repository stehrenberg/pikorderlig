
class RecordingActionHandler:

    def __init__(self, recorder):
        self._recorder = recorder
        self._action_mappings = {
            'recording:start': self._recorder.start_recording,
            'recording:stop': self._recorder.stop_recording,
            'recording:get_status': self._recorder.get_status
        }

    def get_action_mappings(self):
        return self._action_mappings

