from multiprocessing import Process

class Manager(Process):

    def __init__(self):
        Process.__init__(self)
        self.queue          # wird von anderen Prozessen (LEDs, Webserver, Sound) befuellt

    def run(self):
        print("*** Manager started up")
        # spawned Prozesse für Webserver, Recorder, LEDs
        # spawned queues für einzelne prozesse
        # iteriert durch msg queue und arbeitet Auftraege ab


