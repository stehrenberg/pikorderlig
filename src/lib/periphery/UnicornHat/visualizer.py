from multiprocessing import Process
import unicornhat as unicorn
import time

class Visualizer(Process):

    def __init__(self, visualizer_queue):
        Process.__init__(self)

        self._visualizer_queue = visualizer_queue
        self._bootstrap_unicorn()
        self._startup()

    def _bootstrap_unicorn(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.2)
        self.width, self.height = unicorn.get_shape()

    def _startup(self):
        for y in range(self.width):
            for x in range(self.width):
                unicorn.set_pixel(x, y, 255, 0, 0)
                unicorn.show()
                time.sleep(0.01)

        unicorn.off()