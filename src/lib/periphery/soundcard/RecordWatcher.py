from threading import Thread
from time import sleep
class RecordWatcher (Thread):

    def __init__(self, thread_id, name, counter, recording):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter
        self.recording = recording

    def run(self):
        print("*** Watcher started")
        sleep(1)
        is_recording = self.recording.getStatus()
        if is_recording:
            self.recording.stop()

