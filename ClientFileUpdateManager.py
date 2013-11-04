__author__ = 'David'
import time
import os
from GlobalClientCommunicationNetwork import GlobalClientCommunicationNetwork
#TO BE DELETED LATER

class ClientFileUpdateManager():

    def __init__(self,Global):
        self.Global = Global

    def process_events_for_updates(self, eventUpdateList, updateID):
        print eventUpdateList
        for event in eventUpdateList:
            eventType = self.getEventType(event)
            srcPath = self.getFilePath(event)
            #Sets up file for DW to ignore
            self.Global.GlobalClientFileIgnore = self.Global.GlobalClientDirectory + srcPath
            #Call Correct Method Depending On Event Tye
            if eventType == "FileCreatedEvent":
                srcPath = self.getFilePath(event)
                open(self.Global.GlobalClientDirectory + srcPath, 'a').close()
            elif eventType == "FileModifiedEvent":
                print "request file"
                srcPath = self.getFilePath(event)
                self.requestFile(srcPath)
            elif eventType == "FileMovedEvent":
                print "delete file"
                srcPath = self.getFilePathMoved(event)
                os.remove(self.Global.GlobalClientDirectory + srcPath)
            elif eventType == "FileDeletedEvent":
                print "delete file"
                srcPath = self.getFilePath(event)
                os.remove(self.Global.GlobalClientDirectory + srcPath)
            elif eventType == "DirCreatedEvent":
                print "create dir"
                srcPath = self.getFilePath(event)
                #CreateDir
            elif eventType == "DirMovedEvent":
                print "TBD"
                #TBD
            elif eventType == "DirDeletedEvent":
                print "delete dir"
                #DeleteDir
        self.Global.GlobalClientFileIgnore = ""
        #call Operator.unlock(updateID) when finished

    """
    def test_process_events_for_updates(self, updateID):
        print self.Global.GlobalClientUpdateEventQueue
        for event in self.Global.GlobalClientUpdateEventQueue:
            eventType = self.getEventType(event)
            #Call Correct Method Depending On Event Tye
            if eventType == "FileCreatedEvent":
                srcPath = self.getFilePath(event)
                open(self.Global.GlobalClientDirectory + srcPath, 'a').close()
            elif eventType == "FileModifiedEvent":
                srcPath = self.getFilePath(event)
                print "request file"
                self.requestFile(srcPath)
            elif eventType == "FileMovedEvent":
                srcPath = self.getFilePathMoved(event)
                print "delete file"
                os.remove(self.Global.GlobalClientDirectory + srcPath)
            elif eventType == "FileDeletedEvent":
                srcPath = self.getFilePath(event)
                print "delete file"
                os.remove(self.Global.GlobalClientDirectory + srcPath)
            elif eventType == "DirCreatedEvent":
                srcPath = self.getFilePath(event)
                print "create dir"
                os.mkdir(self.Global.GlobalClientDirectory + srcPath)
            elif eventType == "DirMovedEvent":
                srcPath = self.getFilePath(event)
                print "TBD"
                #TBD
            elif eventType == "DirDeletedEvent":
                srcPath = self.getFilePath(event)
                print "delete dir"
                #DeleteDir
        #call Operator.unlock(updateID) when finished
    """

    def getFilePath(self, event):
        return event[event.find("=") + 1:-1]

    def getFilePathMoved(self, event):
        return event[event.find("=") + 1: event.find(",")]

    #Will Be Called By Outside Classes
    def get_file(self, srcPath):
        with open(self.Global.GlobalClientDirectory + srcPath, 'rb') as f:
            content = f.read()
        return content

    def requestFile(self, srcPath):
        self.Global.ClientOperator.request_file(srcPath)

    def getEventType(self, event):
        return event[event.find("<") + 1:event.find(": ")]

    def testRun(self):
        while(True):
            print "Processing:"
            self.test_process_events_for_updates(0)
            time.sleep(1)
