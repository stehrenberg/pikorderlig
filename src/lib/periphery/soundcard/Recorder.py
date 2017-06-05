import time
from multiprocessing import Process
from lib.periphery.soundcard.LineInGrabber import LineInGrabber


class Recorder(Process):
    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self):
        Process.__init__(self)

    def _is_recording(self):
        if "_line_in_grabber" not in dir(self):
            return False

        return self._line_in_grabber.is_recording()

    def get_status(self):
        if self._is_recording():
            status = self._line_in_grabber.status()
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

    def _get_new_file_name(self):
        date_format = '%Y-%m-%d_%H-%M-%S'
        date_as_string = time.strftime(date_format)
        base_path = '/home/pi/recordings/'
        file_ending = '.wav'
        record_file = base_path + 'recording_' + date_as_string + file_ending

        return record_file