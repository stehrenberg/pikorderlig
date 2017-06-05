#!/usr/bin/env python3
import time
from lib.periphery.soundcard.Recorder import Recorder
from lib.webserver.Rest import Rest
from multiprocessing import Queue
from manager.Manager import Manager

def main():
    print("*** Hi there! Starting up...")

    webserver_queue = Queue()
    recorder_queue = Queue()
    manager_queue = Queue()

    webserver = set_up_webserver(webserver_queue, manager_queue)
    recorder = set_up_recorder(recorder_queue, manager_queue)
    manager = set_up_manager(manager_queue)
    manager.set_webserver(webserver, webserver_queue)
    manager.set_recorder(recorder, recorder_queue)

    webserver.start()
    recorder.start()
    manager.start()

def set_up_webserver(webserver_queue, manager_queue):
    return Rest(webserver_queue, manager_queue)

def set_up_recorder(recorder_queue, manager_queue):
    recorder = Recorder(recorder_queue, manager_queue)
    return recorder

def set_up_manager(manager_queue):
    return Manager(manager_queue)

#######################

main()

