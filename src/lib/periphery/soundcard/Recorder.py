import queue
import soundfile as sf
import sounddevice as sd
from threading import Thread
from multiprocessing import Process

from lib.periphery.soundcard.RecordWatcher import RecordWatcher


class Recorder(Process):
    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self, filepath_as_string):
        self._filepath = filepath_as_string
        self._is_recording = False
        self._samplerate = 44100
        self._channels = 2
        self._subtype = "PCM_16"
        self._queue = queue.Queue()
        self.watcher_thread = RecordWatcher(self)
        self.watcher_thread.daemon = True
        self.recording_thread = Thread(target=self.record)

    def start(self):
        self._is_recording = True

        print("*** Recording started!")
        self.recording_thread.start()
        self.watcher_thread.start()

    def record(self):
        with sf.SoundFile(self._filepath,
                mode='x',
                samplerate=self._samplerate,
                channels=self._channels,
                subtype=self._subtype) as file:
            with sd.InputStream(samplerate=self._samplerate,
                                device=0,
                                channels=self._channels,
                                callback=self._callback):
                while self._is_recording:
                    file.write(self._queue.get())

    def stop(self):
        print("*** Recording stopped")
        self._is_recording = False

    def getStatus(self):
        return self._is_recording

    def _callback(self, indata, frames, time, status):
        self._queue.put(indata.copy())


    def sigIntHandler(self, signum, stack):
        print("*** Keyboard interrupt, stopping recording")
        self.stop()



