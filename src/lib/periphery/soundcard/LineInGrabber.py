import queue
import soundfile as sf
import sounddevice as sd
import time
from threading import Thread


class LineInGrabber(Thread):
    _is_recording = False
    _filepath = ''
    _current_slice = 0
    _current_slice_start = 0.0
    _slice_length = 7200.0  # seconds
    _samplerate = 44100
    _channels = 2
    _subtype = "PCM_16"

    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self, file_information):
        Thread.__init__(self)
        self._file_information = file_information
        self._recording_queue = queue.Queue()
        self._recording_start = 0

    def run(self):
        self._is_recording = True
        self.record()

    def _get_current_slice_as_string(self):
        return str(self._current_slice)

    def _get_current_file_name(self):
        return self._file_information['file_path'] +\
               '-part-' + self._get_current_slice_as_string() +\
               self._file_information['file_ending']

    def _create_next_sound_file(self):
        self._filepath = self._get_current_file_name()
        self._soundfile = sf.SoundFile(self._filepath,
                                       mode='x',
                                       samplerate=self._samplerate,
                                       channels=self._channels,
                                       subtype=self._subtype)

        self._reset_slice_length()

    def record(self):
        self._recording_start = time.time()
        self._create_next_sound_file()
        print('*** Recording ', self._filepath)

        # with self._soundfile as file:
        with sd.InputStream(samplerate=self._samplerate,
                            device=0,
                            channels=self._channels,
                            callback=self._input_stream_callback):
            while self._is_recording:
                self._soundfile.write(self._recording_queue.get())
        return

    def _rotate_slice(self):
        self._current_slice += 1
        self._create_next_sound_file()
        print('*** Recording new slice ', self._filepath)

    def stop(self):
        self._is_recording = False
        time.sleep(1)
        self._soundfile.close()
        print("*** Stopped recording ", self._filepath)

    def _input_stream_callback(self, indata, frames, recording_time, status):
        if status:
            print("*** Error while recording: ", status)

        self._store_slice_start(recording_time)

        if self._is_slice_length_reached(recording_time):
            self._rotate_slice()

        self._recording_queue.put(indata.copy())

    def get_status(self):
        return {
            "recording": self._is_recording,
            "file": self._filepath,
            "recording_start": self._recording_start
        }

    def is_recording(self):
        return self._is_recording

    def _is_slice_length_reached(self, recording_time):
        return recording_time.currentTime - self._current_slice_start >= self._slice_length

    def _reset_slice_length(self):
        self._current_slice_start = 0.0  # will be set first time in the input callback

    def _store_slice_start(self, recording_time):
        if self._current_slice_start == 0.0:
            self._current_slice_start = recording_time.currentTime

    def sigIntHandler(self, signum, stack):
        print("*** Keyboard interrupt, stopping recording")
        self.stop()



