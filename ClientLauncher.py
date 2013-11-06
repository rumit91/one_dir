__author__ = 'Timur'
import Queue
import Operator
import DirectoryWatcher
import socket
import threading
from ClientGlobal import ClientGlobal

class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


serverEventPort = 12345
serverFileRequestPort = 12346
serverFilePort = 12347
#serverHostName = 172.27.99.193
serverHostName = socket.gethostbyname(socket.getfqdn())
clientHostName = '172.27.99.194'

localGlobal = ClientGlobal()
clientOperator = Operator.Operator(serverEventPort, serverFileRequestPort, serverFilePort, serverHostName, clientHostName, localGlobal)
localGlobal.ClientOperator = clientOperator
clientDirectoryWatcher = DirectoryWatcher.DirectoryWatcher(localGlobal)
print 'about to run the directoryWatcher'
ClientDirectoryWatcherThread = myThread(clientDirectoryWatcher)
ClientDirectoryWatcherThread.start()
print 'about to run the clientOperator'
ClientOperatorThread1 = myThread(clientOperator.myEventDispatcher)
ClientOperatorThread1.start()
ClientOperatorThread2 = myThread(clientOperator.myFileRequestListener)
ClientOperatorThread2.start()


