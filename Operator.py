__author__ = 'Timur'
import communicator
import Queue
from ClientFileUpdateManager import ClientFileUpdateManager
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

			#self.GlobalClientEventQueue.join()	   # block until all tasks are done


#server
class EventListener:
	class myReceiver(communicator.Receiver):
		def __init__(self, host_name, port, ServerEventQueue):
			self.host_name = host_name
			self.port = port
			self.ServerEventQueue = ServerEventQueue

		def dispatch(self, message):
			print ["New Event: ", message]
			self.ServerEventQueue.put(message)

	def __init__(self, port, host_name, ServerEventQueue):
		self.port = port
		self.host_name = host_name
		self.myReceiver = self.myReceiver(self.host_name, self.port, ServerEventQueue)

	def run(self):
		self.myReceiver.setup()
		self.myReceiver.spin()


#server
class FileRequestDispatcher:
	def __init__(self, port, host_name, filePath):
		self.port = port
		self.host_name = host_name
		self.num_worker_threads = 1
		self.myFilePath = filePath
		self.myMessenger = communicator.Messenger(self.host_name, self.port)

	def request_file(self):
		self.myMessenger.send(self.myFilePath)


#local
class FileRequestListener:
	class myReceiver(communicator.Receiver):
		def dispatch(self, message):
			print ["New File Request: ", message]
			CFUM = ClientFileUpdateManager(self.globalInfo)
			myFileDispatcher = FileDispatcher(self.port + 1, self.host_name, message, CFUM)
			myFileDispatcher.get_file()


	def __init__(self, port, host_name, clientGlobal):
		self.clientGlobal = clientGlobal
		self.port = port
		self.host_name = host_name
		self.myReceiver = self.myReceiver(self.host_name, self.port, clientGlobal)

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
			print "WRITING"
			with open(self.globalInfo.GlobalServerDirectory + self.globalInfo.GlobalUserID + "\\OneDir\\" + self.globalInfo.GlobalCurSrcPath, "wb") as f: 
				f.write(message)

	def __init__(self, port, host_name, serverGlobal):
		self.port = port
		self.host_name = host_name
		self.serverGlobal = serverGlobal
		self.myReceiver = self.myReceiver(self.host_name, self.port, self.serverGlobal)

	def run(self):
		self.myReceiver.setup()
		self.myReceiver.spin()


class Operator:
	def __init__(self, event_port, file_request_port, file_port, local_host_name, target_host_name, clientGlobal):
		self.local_host_name = local_host_name
		self.target_host_name = target_host_name
		self.event_port = event_port
		self.file_request_port = file_request_port
		self.file_port = file_port
		self.clientGlobal = clientGlobal
		self.GlobalEventQueue = clientGlobal.GlobalClientEventQueue
		self.myEventDispatcher = EventDispatcher(self.event_port, self.target_host_name, self.GlobalEventQueue)
		self.myEventListener = EventListener(self.event_port, self.local_host_name, self.GlobalEventQueue)
		self.myFileListener = FileListener(self.file_port, self.target_host_name, self.clientGlobal)
		self.myFileRequestListener = FileRequestListener(self.file_request_port, self.local_host_name, self.clientGlobal)


	def request_file(self, srcPath):
		myFileRequestDispatcher = FileRequestDispatcher(self.file_request_port, self.target_host_name, srcPath)
		myFileRequestDispatcher.request_file()
		print "Requesting File"

