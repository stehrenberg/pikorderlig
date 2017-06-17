#!/usr/bin/env python3
import time
from lib.periphery.soundcard.Recorder import Recorder
from lib.webserver.Rest import Rest
from lib.periphery.unicornHat.Visualizer import Visualizer
from multiprocessing import Queue
from manager.Manager import Manager
from manager.RecordingActionHandler import RecordingActionHandler
from manager.WebActionHandler import WebActionHandler
from manager.VisualizerActionHandler import VisualizerActionHandler


def main():
    print("*** Hi there! Starting up...")

    webserver_queue = Queue()
    recorder_queue = Queue()
    manager_queue = Queue()
    visualizer_queue = Queue()

    webserver = set_up_webserver(webserver_queue, manager_queue)
    recorder = set_up_recorder(recorder_queue, manager_queue)
    manager = set_up_manager(manager_queue)
    visualizer = set_up_visualizer(visualizer_queue)

    manager.set_webserver(webserver, webserver_queue)
    manager.set_recorder(recorder, recorder_queue)

    recording_action_handler = RecordingActionHandler(recorder)
    web_action_handler = WebActionHandler(recorder, webserver_queue)
    visualizer_action_handler = VisualizerActionHandler(visualizer_queue)
    manager.add_action_mappings(recording_action_handler)
    manager.add_action_mappings(web_action_handler)
    manager.add_action_mappings(visualizer_action_handler)

    webserver.start()
    recorder.start()
    manager.start()
    visualizer.start()

def set_up_webserver(webserver_queue, manager_queue):
    return Rest(webserver_queue, manager_queue)

def set_up_recorder(recorder_queue, manager_queue):
    recorder = Recorder(recorder_queue, manager_queue)
    return recorder

def set_up_manager(manager_queue):
    return Manager(manager_queue)

def set_up_visualizer(visualizer_queue):
    return Visualizer(visualizer_queue)

#######################

main()

