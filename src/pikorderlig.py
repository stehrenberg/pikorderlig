#!/usr/bin/env python3
import time
from lib.periphery.soundcard.Recorder import Recorder
from lib.webserver.Rest import Rest
from multiprocessing import Queue
from manager.Manager import Manager

def main():
    print("*** Hi there! Starting up...")
    webserver_queue = Queue()

    print("*** Starting Webserver")
    webserver = setup_webserver(webserver_queue)
    webserver.start()

    print("*** Starting Recorder")
    recorder = set_up_recorder()
    recorder.start()

    print("*** Starting Manager")
    manager = setup_manager()

    # print(current_time())
    # time.sleep(5)
    # recording_time = 6 * 3600
    # print("*** Recording for seconds: ", recording_time)
    # time.sleep(recording_time)
    # recorder.stop()
    # print(current_time())

def set_up_recorder():
    recorder = Recorder(filepath_as_string=build_file_path())

    return recorder

def current_time():
    date_format = '%Y-%m-%d %H:%M:%S'
    return time.strftime(date_format)

def build_file_path():
    date_format = '%Y-%m-%d_%H-%M-%S'
    date_as_string = time.strftime(date_format)
    base_path = '/home/pi/recordings/'
    file_ending = '.wav'
    record_file = base_path + 'recording_' + date_as_string + file_ending

    return record_file

def setup_webserver(webserver_queue):
    return Rest(webserver_queue)

def setup_manager():
    return Manager()

#######################

main()

