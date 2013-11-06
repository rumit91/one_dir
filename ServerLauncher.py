__author__ = 'Timur'
import Queue
import Operator
import threading
import socket
import ServerFileUpdateManager
from ServerGlobal import ServerGlobal

class myThread(threading.Thread):
	def __init__(self, run_object):
		threading.Thread.__init__(self)
		self.run_object = run_object

	def run(self):
		print "Starting"
		self.run_object.run()
        print "Ending"


clientEventPort = 12345
clientFileRequestPort = 12346
clientFilePort = 12347
clientHostName = socket.gethostbyname(socket.getfqdn())
serverHostName = socket.gethostbyname(socket.getfqdn())

serverGlobal = ServerGlobal()

serverOperator = Operator.Operator(clientEventPort, clientFileRequestPort,clientFilePort, clientHostName, serverHostName, serverGlobal)
serverGlobal.ServerOperator = serverOperator
serverFileUpdateManager = ServerFileUpdateManager.ServerFileUpdateManager(serverGlobal)
print 'about to run the serverOperator'
ClientOperatorThread1 = myThread(serverOperator.myEventListener)
ClientOperatorThread1.start()
ClientOperatorThread2 = myThread(serverOperator.myFileListener)
ClientOperatorThread2.start()
print 'about to run the serverFileUpdateManager'
serverFileUpdateManagerThread = myThread(serverFileUpdateManager)
serverFileUpdateManagerThread.start()

