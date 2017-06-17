from multiprocessing import Process
from random import randint
import time

class Visualizer(Process):

    def __init__(self, visualizer_queue):
        Process.__init__(self)

        self._visualizer_queue = visualizer_queue
        #self._bootstrap_unicorn()
        #self._startup()

    def run(self):
        import unicornhat as unicorn

        self._bootstrap_unicorn(unicorn)
        self._startup(unicorn)
        print('*** Unicorn started up')

        while True:
            info = self._visualizer_queue.get()
            if info == 'recording:heartbeat':
                unicorn.set_pixel(7, 3, 0, 0, 0)
                unicorn.show()
                time.sleep(2)
                unicorn.set_pixel(7, 3, 255, 0, 0)
                unicorn.show()
            elif info == 'recording:stopped':
                unicorn.set_pixel(7, 3, 0, 0, 0)
                unicorn.show()
            elif info == 'recording:volume':
                x = randint(0, 6)
                y = randint(0, 2)
                red = randint(1, 255)
                green = randint(1, 255)
                blue = randint(1, 255)
                unicorn.set_pixel(x, y, red, green, blue)
                unicorn.show()


    def _bootstrap_unicorn(self, unicorn):
        unicorn.set_layout(unicorn.PHAT)
        unicorn.rotation(0)
        unicorn.brightness(0.2)
        self.width, self.height = unicorn.get_shape()
        print('Unicorn has width: ', self.width, ' and height: ', self.height)

    def _startup(self, unicorn):
        for y in range(self.width):
            for x in range(self.width):
                unicorn.set_pixel(x, y, 0, 0, 255)
                unicorn.show()
                time.sleep(0.01)

        for y in range(self.width):
            for x in range(self.width):
                unicorn.set_pixel(x, y, 0, 0, 0)
                unicorn.show()
                time.sleep(0.01)