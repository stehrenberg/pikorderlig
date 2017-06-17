import queue
import soundfile as sf
import sounddevice as sd
import time
from threading import Thread
import numpy as np

class LineInGrabber(Thread):
    _is_recording = False
    _is_soundfile_writable = False
    _filepath = ''
    _current_slice = 0
    _current_slice_start = 0.0
    _slice_length = 14400.0  # seconds
    _heartbeat_rate = 5.0 # seconds
    _last_heartbeat = 0.0
    _samplerate = 44100
    _channels = 2
    _subtype = "PCM_16"

    """
    Represents a recording instance that records the current line-in signal as .WAV file.
    """

    def __init__(self, file_information, manager_queue):
        Thread.__init__(self)
        self._file_information = file_information
        self._recording_queue = queue.Queue()
        self._recording_start = 0
        self._manager_queue = manager_queue
        delta_f = (2000 - 100) / (8 - 1) # /high - low / columns - 1
        self._fftsize = np.ceil(self._samplerate / delta_f).astype(int)

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
        self._is_soundfile_writable = True

    def record(self):
        self._recording_start = time.time()
        self._create_next_sound_file()
        print('*** Recording ', self._filepath)

        # with self._soundfile as file:
        with sd.InputStream(samplerate=self._samplerate,
                            device=0,
                            channels=self._channels,
                            callback=self._input_stream_callback):
            self._send_heartbeat()
            while self._is_recording:
                self._store_to_soundfile()
        return

    def _store_to_soundfile(self):
        if self._is_soundfile_writable:
            self._soundfile.write(self._recording_queue.get())

    def _rotate_slice(self):
        self._is_soundfile_writable = False
        self._current_slice += 1
        self._create_next_sound_file()
        print('*** Recording new slice ', self._filepath)

    def stop(self):
        self._is_recording = False
        time.sleep(1)
        self._soundfile.close()
        self._manager_queue.put('recording:stopped')
        print("*** Stopped recording ", self._filepath)

    def _input_stream_callback(self, indata, frames, recording_time, status):
        if status:
            print("*** Error while recording: ", status)

        self._store_slice_start(recording_time)

        if self._is_slice_length_reached(recording_time):
            self._rotate_slice()

        if self._is_heartbeat_due(recording_time):
            self._send_heartbeat()
            self._store_last_heartbeat(recording_time)

        self._recording_queue.put(indata.copy())
        #self._calculate_and_send_fft(indata)

    def _calculate_and_send_fft(self, indata):
        #magnitude = np.abs(np.fft.rfft(indata[:, 0], n=self._fftsize))
        #magnitude *= 10 / self._fftsize # first parameter: gain
        # Could not test with real data on first coding so just send a volume event
        self._manager_queue.put('recording:volume')

    def _send_heartbeat(self):
        self._manager_queue.put('recording:heartbeat')

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

    def _is_heartbeat_due(self, recording_time):
        return recording_time.currentTime - self._last_heartbeat >= self._heartbeat_rate

    def _reset_slice_length(self):
        self._current_slice_start = 0.0  # will be set first time in the input callback

    def _store_slice_start(self, recording_time):
        if self._current_slice_start == 0.0:
            self._current_slice_start = recording_time.currentTime

    def _store_last_heartbeat(self, recording_time):
        self._last_heartbeat = recording_time.currentTime

    def sigIntHandler(self, signum, stack):
        print("*** Keyboard interrupt, stopping recording")
        self.stop()



