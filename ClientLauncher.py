__author__ = 'Timur'
import Queue
import Operator
import DirectoryWatcher
import threading


class Global:
    def __init__(self):
        self.GlobalClientEventQueue = Queue.Queue()
        self.GlobalClientDirectory = "C:/Users/Timur/Desktop/OneDir"
        self.GlobalClientFileIgnore = ""


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


serverPort = 12345
serverHostName = '192.168.20.11'

localGlobal = Global()
clientOperator = Operator.Operator(serverPort, serverHostName, localGlobal.GlobalClientEventQueue)
clientDirectoryWatcher = DirectoryWatcher.DirectoryWatcher(localGlobal)
print 'about to run the directoryWatcher'
ClientDirectoryWatcherThread = myThread(clientDirectoryWatcher)
ClientDirectoryWatcherThread.start()
print 'about to run the clientOperator'
ClientOperatorThread = myThread(clientOperator.myEventDispatcher)
ClientOperatorThread.start()

