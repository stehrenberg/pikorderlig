from threading import Thread
from time import sleep

class RecordWatcher(Thread):

    def __init__(self, record):
        Thread.__init__(self)
        self.record = record

    def run(self):
        print("*** Watcher started")
        while True:
            sleep(1)
            is_recording = self.record.getStatus()
            print("*** is_recording = ", is_recording)
            if not is_recording:
                self.record.stop()

