__author__ = 'Timur'
import Queue
import Operator
import threading
import ServerFileUpdateManager


class Global:
    def __init__(self):
        self.GlobalClientEventQueue = Queue.Queue()
        self.GlobalClientDirectory = "C:/Users/Timur/Desktop/OneDir/1"
        self.GlobalClientFileIgnore = ""


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


clientPort = 12345
clientHostName = '192.168.20.11'
serverGlobal = Global()
serverOperator = Operator.Operator(clientPort, clientHostName, serverGlobal.GlobalClientEventQueue)
serverFileUpdateManager = ServerFileUpdateManager.ServerFileUpdateManager(serverGlobal)
print 'about to run the serverOperator'
ClientOperatorThread = myThread(serverOperator.myEventListener)
ClientOperatorThread.start()
print 'about to run the serverFileUpdateManager'
serverFileUpdateManagerThread = myThread(serverOperator.myEventListener)
serverFileUpdateManagerThread.start()

