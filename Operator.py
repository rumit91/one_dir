__author__ = 'Timur'
import communicator
import Queue
from threading import Thread


class Operator:
    def __init__(self, port, host_name, GlobalClientEventQueue):
        self.port = port
        self.host_name = host_name
        self.GlobalClientEventQueue = GlobalClientEventQueue
        self.num_worker_threads = 1;

    def do_work(self, item):
        print "got an item"
        myMessenger = communicator.Messenger(self.port, self.GlobalClientEventQueue)
        myMessenger.send(item)

    def run(self):
        def worker():
            while True:
                item = self.GlobalClientEventQueue.get()
                self.do_work(item)
                self.GlobalClientEventQueue.task_done()

        for i in range(self.num_worker_threads):
            t = Thread(target=worker())
            t.daemon = True
            t.start()

            #self.GlobalClientEventQueue.join()       # block until all tasks are done