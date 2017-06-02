import soundfile as sf
import sounddevice as sd

class Recorder:

    def __init__(self, filepath_as_string):
        self.filepath = filepath_as_string

    def start(self):
        print("*** Recording started!")
        print(sd.query_devices())

    def stop(self):
        print("*** Recording stopped")