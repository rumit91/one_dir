__author__ = 'Timur'
import communicator
import Queue
from threading import Thread


#local
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


#server
class EventListener:
    class myReceiver(communicator.Receiver):
        def __init__(self, host_name, port, ServerEventQueue):
            communicator.Receiver.__init__(self, host_name, port)
            self.ServerEventQueue = ServerEventQueue

        def dispatch(self, message):
            print ["New Event: ", message]

    def __init__(self, port, host_name):
        self.port = port
        self.host_name = host_name
        ServerEventQueue = []
        self.myReceiver = self.myReceiver(self.host_name, self.port, ServerEventQueue)

    def run(self):
        self.myReceiver.setup()
        self.myReceiver.spin()


#server
class FileRequestDispatcher:
    def __init__(self, port, host_name, filePath, fileUpdateManager):
        self.port = port
        self.host_name = host_name
        self.num_worker_threads = 1
        self.myFilePath = filePath
        self.myMessenger = communicator.Messenger(self.host_name, self.port)
        self.myFileUpdateManager = fileUpdateManager

    def get_file(self):
        myFile = self.myFileUpdateManager.get_file(self.myFilePath)
        self.myMessenger.send(myFile)


#local
class FileRequestListener:
    class myReceiver(communicator.Receiver):
        def dispatch(self, message):
            print ["New File Request: ", message]

    def __init__(self, port, host_name):
        self.port = port
        self.host_name = host_name
        self.myReceiver = self.myReceiver(self.host_name, self.port)

    def run(self):
        self.myReceiver.setup()
        self.myReceiver.spin()


#local
class FileDispatcher:
    def __init__(self, port, host_name, filePath, fileUpdateManager):
        self.port = port
        self.host_name = host_name
        self.num_worker_threads = 1
        self.myFilePath = filePath
        self.myMessenger = communicator.Messenger(self.host_name, self.port)
        self.myFileUpdateManager = fileUpdateManager

    def get_file(self):
        myFile = self.myFileUpdateManager.get_file(self.myFilePath)
        self.myMessenger.send(myFile)


#sever
class FileListener:
    class myReceiver(communicator.Receiver):
        def dispatch(self, message):
            print ["New File: ", message]

    def __init__(self, port, host_name):
        self.port = port
        self.host_name = host_name
        self.myReceiver = self.myReceiver(self.host_name, self.port)

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
