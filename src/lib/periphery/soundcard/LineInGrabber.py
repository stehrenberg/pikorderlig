import queue
import soundfile as sf
import sounddevice as sd
import time
from threading import Thread


class LineInGrabber(Thread):
    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self, filepath_as_string):
        Thread.__init__(self)
        self._filepath = filepath_as_string
        self._is_recording = False
        self._samplerate = 44100
        self._channels = 2
        self._subtype = "PCM_16"
        self._queue = queue.Queue()
        self._recording_start = 0

    def run(self):
        self._is_recording = True
        self.record()

    def record(self):
        print('Recording ', self._filepath)

        self._recording_start = time.time()
        self._soundfile = sf.SoundFile(self._filepath,
                                       mode='x',
                                       samplerate=self._samplerate,
                                       channels=self._channels,
                                       subtype=self._subtype)

        with self._soundfile as file:
            with sd.InputStream(samplerate=self._samplerate,
                                device=0,
                                channels=self._channels,
                                callback=self._callback):
                while self._is_recording:
                    file.write(self._queue.get())
        return

    def stop(self):
        self._is_recording = False
        time.sleep(1)
        self._soundfile.close()
        print("*** Stopped recording ", self._filepath)

    def is_recording(self):
        return self._is_recording

    def _callback(self, indata, frames, time, status):
        self._queue.put(indata.copy())

    def get_status(self):
        return {
            "recording": self._is_recording,
            "file": self._filepath,
            "recording_start": self._recording_start
        }

    def sigIntHandler(self, signum, stack):
        print("*** Keyboard interrupt, stopping recording")
        self.stop()



