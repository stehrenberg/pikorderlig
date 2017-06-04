from multiprocessing import Process
from lib.periphery.soundcard.LineInGrabber import LineInGrabber


class Recorder(Process):
    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self, filepath_as_string):
        Process.__init__(self)
        self._filepath = filepath_as_string
        self._line_in_grabber = LineInGrabber(filepath_as_string)


    def run(self):
        self._line_in_grabber.run()

    def stop(self):
        self._line_in_grabber.stop()

