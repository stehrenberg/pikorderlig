#!/usr/bin/env python
import time
from lib.periphery.soundcard.Recorder import Recorder

print("*** Hi there! Starting up...")

date_format = '%Y-%m-%d_%H-%M-%S'
date_as_string = time.strftime(date_format)
record_file = 'recording_' + date_as_string

print("time.strftime() is: " + date_as_string)
print("file name is: " + record_file)
recorder = Recorder(record_file)

recorder.start()
time.sleep(5)
recorder.stop()
