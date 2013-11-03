__author__ = 'Timur'
import communicator
import Queue
from threading import Thread


class EventDispatcher:
    def __init__(self, port, host_name, GlobalEventQueue):
        self.port = port
        self.host_name = host_name
        self.GlobalEventQueue = GlobalEventQueue
        self.num_worker_threads = 1
        self.myMessenger = communicator.Messenger(self.host_name, self.port)

    def do_work(self, item):
        print "got an item"
        self.myMessenger.send(item)

    def run(self):
        def worker():
            while True:
                item = self.GlobalEventQueue.get()
                self.do_work(item)
                self.GlobalEventQueue.task_done()
        for i in range(self.num_worker_threads):
            t = Thread(target=worker())
            t.daemon = True
            t.start()

            #self.GlobalClientEventQueue.join()       # block until all tasks are done


class EventListener:
    def __init__(self, port, host_name):
        self.port = port
        self.host_name = host_name
        self.myReceiver = communicator.Receiver(self.host_name, self.port)

    def run(self):
        self.myReceiver.setup()
        self.myReceiver.spin()


class Operator:
    def __init__(self, port, host_name, GlobalClientEventQueue):
        self.port = port
        self.host_name = host_name
        self.GlobalEventQueue = GlobalClientEventQueue
        self.myEventDispatcher = EventDispatcher(self.port, self.host_name, self.GlobalEventQueue)
        self.myEventListener = EventListener(self.port, self.host_name)
