from multiprocessing import Process

class Manager(Process):

    def __init__(self, recorder_queue):
        Process.__init__(self)
        self.recorder_queue = recorder_queue

    def run(self):
        print("*** Manager started up")
        # spawned Prozesse für Webserver, Recorder, LEDs
        # spawned queues für einzelne prozesse
        # iteriert durch msg queue und arbeitet Auftraege ab


