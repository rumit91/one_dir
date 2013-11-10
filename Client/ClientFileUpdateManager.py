__author__ = 'David'
import time
import os
#TO BE DELETED LATER

class ClientFileUpdateManager():

    def __init__(self, global_info):
        self.global_info = global_info

    def process_events_for_updates(self, eventUpdateList, updateID):
        print eventUpdateList
        for event in eventUpdateList:
            eventType = self.getEventType(event)
            srcPath = self.getFilePath(event)
            #Sets up file for DW to ignore
            self.global_info.client_global_file_ignore = self.global_info.client_global_directory + srcPath
            #Call Correct Method Depending On Event Tye
            if eventType == "FileCreatedEvent":
                print "request file"
                srcPath = self.getFilePath(event)
                self.requestFile(srcPath)
            elif eventType == "FileModifiedEvent":
                print "request file"
                srcPath = self.getFilePath(event)
                self.requestFile(srcPath)
            elif eventType == "FileMovedEvent":
                print "delete file"
                srcPath = self.getFilePathMoved(event)
                os.remove(self.global_info.client_global_directory + srcPath)
            elif eventType == "FileDeletedEvent":
                print "delete file"
                srcPath = self.getFilePath(event)
                os.remove(self.global_info.client_global_directory + srcPath)
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
        self.global_info.client_global_file_ignore = ""
        #call Operator.unlock(updateID) when finished

    """
    def test_process_events_for_updates(self, updateID):
        print self.Global.GlobalClientUpdateEventQueue
        for event in self.Global.GlobalClientUpdateEventQueue:
            eventType = self.getEventType(event)
            #Call Correct Method Depending On Event Tye
            if eventType == "FileCreatedEvent":
                srcPath = self.getFilePath(event)
                open(self.Global.client_global_directory + srcPath, 'a').close()
            elif eventType == "FileModifiedEvent":
                srcPath = self.getFilePath(event)
                print "request file"
                self.requestFile(srcPath)
            elif eventType == "FileMovedEvent":
                srcPath = self.getFilePathMoved(event)
                print "delete file"
                os.remove(self.Global.client_global_directory + srcPath)
            elif eventType == "FileDeletedEvent":
                srcPath = self.getFilePath(event)
                print "delete file"
                os.remove(self.Global.client_global_directory + srcPath)
            elif eventType == "DirCreatedEvent":
                srcPath = self.getFilePath(event)
                print "create dir"
                os.mkdir(self.Global.client_global_directory + srcPath)
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
        try:
            with open(self.global_info.client_global_directory + srcPath, 'rb') as f:
                content = f.read()
        except:
            content = ""
        return content

    def requestFile(self, srcPath):
        self.global_info.ClientOperator.request_file(srcPath)

    def getEventType(self, event):
        return event[event.find("<") + 1:event.find(": ")]
