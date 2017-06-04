#!/usr/bin/env python3
import time
from lib.periphery.soundcard.Recorder import Recorder

print("*** Hi there! Starting up...")

date_format = '%Y-%m-%d_%H-%M-%S'
date_as_string = time.strftime(date_format)
base_path = '/home/pi/recordings/'
file_ending = '.wav'
record_file = 'recording_' + date_as_string + file_ending
recorder = Recorder(record_file)


print("time.strftime() is: " + date_as_string)
print("file name is: " + record_file)

recorder.start()
time.sleep(10)
recorder.stop()
