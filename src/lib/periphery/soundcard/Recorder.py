import soundfile as sf
import sounddevice as sd
import queue

class Recorder:

    def __init__(self, filepath_as_string):
        self._filepath = filepath_as_string
        self._is_recording = False
        self._samplerate = 44100
        self._channels = 2
        self._subtype = "PCM_16"
        self._queue = queue.Queue()

    def start(self):
        print("*** Recording started!")
        print(sd.query_devices())
        self._is_recording = True

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

    def _callback(self, indata, frames, time, status):
        self._queue.put(indata.copy())



