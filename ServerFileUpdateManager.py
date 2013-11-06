__author__ = 'David'
import time
import os
from GlobalServerCommunicationNetwork import GlobalServerCommunicationNetwork
from ClientFileUpdateManager import ClientFileUpdateManager
from threading import Thread


class ServerFileUpdateManager():
	def __init__(self,Global):
		self.Global = Global

	def run(self):
		def worker():
			while True:
				item = self.Global.GlobalClientEventQueue.get()
				self.process_event_for_updates(item, 1)
				self.Global.GlobalClientEventQueue.task_done()
		for i in range(1):
			t = Thread(target=worker())
			t.daemon = True
			t.start()

	def process_event_for_updates(self, event, updateID):
		with open(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\EventLog.txt", "a") as f:
			f.write("\n" + event)
		eventType = self.getEventType(event)
        #Call Correct Method Depending On Event Tye
		if eventType == "FileCreatedEvent":
			srcPath = self.getServerFilePath(event)
			print "writing file"
			open(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath, 'a').close()
		elif eventType == "FileModifiedEvent":
			print "request file"
			srcPath = self.getServerFilePath(event)
			self.Global.GlobalCurSrcPath = srcPath
			self.requestFile(srcPath)
		elif eventType == "FileMovedEvent":
			print "delete file"
			srcPath = self.getServerFilePathMoved(event)
			os.remove(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath)
		elif eventType == "FileDeletedEvent":
			print "delete file"
			srcPath = self.getServerFilePath(event)
			os.remove(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath)
		elif eventType == "DirCreatedEvent":
			print "create dir"
			srcPath = self.getServerFilePath(event)
			os.mkdir(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath)
		elif eventType == "DirMovedEvent":
			print "TBD"
			#TBD
		elif eventType == "DirDeletedEvent":
			print "delete dir"
            #DeleteDir
    #call Operator.unlock(updateID) when finished

	"""
    def test_process_events_for_updates(self, updateID):
        print self.Global.GlobalClientEventQueue
        for event in self.Global.GlobalClientEventQueue:
            with open(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\EventLog.txt", "a") as f:
                f.write("\n" + event)
            eventType = self.getEventType(event)
            #Call Correct Method Depending On Event Tye
            if eventType == "FileCreatedEvent":
                srcPath = self.getServerFilePath(event)
                open(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath, 'a').close()
            elif eventType == "FileModifiedEvent":
                srcPath = self.getServerFilePath(event)
                print "request file"
                file = self.requestFile(srcPath)
                with open(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath, "wb") as f:
                    f.write(file)
            elif eventType == "FileMovedEvent":
                srcPath = self.getServerFilePathMoved(event)
                print "delete file"
                os.remove(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath)
            elif eventType == "FileDeletedEvent":
                srcPath = self.getServerFilePath(event)
                print "delete file"
                os.remove(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath)
            elif eventType == "DirCreatedEvent":
                srcPath = self.getServerFilePath(event)
                print "create dir"
                os.mkdir(self.Global.GlobalServerDirectory + self.Global.GlobalUserID + "\\OneDir\\" + srcPath)
            elif eventType == "DirMovedEvent":
                srcPath = self.getServerFilePath(event)
                print "TBD"
                #TBD
            elif eventType == "DirDeletedEvent":
                srcPath = self.getServerFilePath(event)
                print "delete dir"
                #DeleteDir
        self.Global.GlobalClientEventQueue = []
        #call Operator.unlock(updateID) when finished
	"""

	def getServerFilePath(self, event):
		return event[event.find("=") + 1:-1]

	def getServerFilePathMoved(self, event):
		return event[event.find("=") + 1: event.find(",")]

	def requestFile(self, srcPath):
		self.Global.ServerOperator.request_file(srcPath)
		print "requesting file"

	def getEventType(self, event):
		return event[event.find("<") + 1:event.find(": ")]

	def testRun(self):
		while(True):
			print "Processing:"
			self.test_process_events_for_updates(0)
			time.sleep(1)
