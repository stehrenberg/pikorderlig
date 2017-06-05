import time
from multiprocessing import Process
from lib.periphery.soundcard.LineInGrabber import LineInGrabber


class Recorder(Process):
    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self, recorder_queue, manager_queue):
        Process.__init__(self)
        self._recorder_queue = recorder_queue
        self._manager_queue = manager_queue

    def run(self):
        print("*** Starting Recorder")

    def get_status(self):
        if self._is_recording():
            status = self._line_in_grabber.get_status()
        else:
            status = {
                "recording": False,
                "file": None,
                "recording_start": None
            }
        return status

    def start_recording(self):
        if not self._is_recording():
            filepath = self._get_new_file_name()
            self._line_in_grabber = LineInGrabber(filepath)
            self._line_in_grabber.start()

    def stop_recording(self):
        if self._is_recording():
            self._line_in_grabber.stop()
            self._line_in_grabber.join()
            del self._line_in_grabber

############## Helpers ##############

    def _is_recording(self):
        status = False

        if "_line_in_grabber" in dir(self):
            status = self._line_in_grabber.is_recording()

        return status

    def _get_new_file_name(self):
        date_format = '%Y-%m-%d_%H-%M-%S'
        date_as_string = time.strftime(date_format)
        base_path = '/home/pi/recordings/'
        file_ending = '.wav'
        record_file = base_path + 'recording_' + date_as_string + file_ending

        return record_file