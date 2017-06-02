import soundfile
import sounddevice

class Recorder:

    def __init__(self, filepath_as_string):
        self.filepath = filepath_as_string

    def start(self):
        print("*** Recording started!")

    def stop(self):
        print("*** Recording stopped")