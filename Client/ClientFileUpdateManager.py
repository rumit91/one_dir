__author__ = 'David'
import time
import os
from threading import Thread
#TO BE DELETED LATER

class ClientFileUpdateManager():

    def __init__(self, global_info):
        self.global_info = global_info

    def run(self):
        def worker():
            while True:
                item = self.global_info.client_global_update_queue.get()
                self.process_event_for_updates(item)
                time.sleep(.5)
                self.global_info.client_global_update_queue.task_done()

        for i in range(1):
            t = Thread(target=worker())
            t.daemon = True
            t.start()

    def process_event_for_updates(self, item):
        self.global_info.updating = True
        eventType = self.getEventType(item)
        srcPath = self.getFilePath(item)
        #Sets up file for DW to ignore
        self.global_info.client_global_file_ignore = self.global_info.client_global_directory + srcPath
        #Call Correct Method Depending On Event Tye
        if eventType == "FileCreatedEvent":
            print "request file"
            srcPath = self.getFilePath(item)
            self.global_info.global_cur_src_path = srcPath
            self.requestFile(srcPath)
        elif eventType == "FileModifiedEvent":
            print "request file"
            srcPath = self.getFilePath(item)
            self.global_info.global_cur_src_path = srcPath
            self.requestFile(srcPath)
        elif eventType == "FileMovedEvent":
            print "delete file"
            srcPath = self.getFilePathMoved(item)
            try:
                os.remove(self.global_info.client_global_directory + srcPath)
            except:
                print ""
        elif eventType == "FileDeletedEvent":
            print "delete file"
            srcPath = self.getFilePath(item)
            try:
                os.remove(self.global_info.client_global_directory + srcPath)
            except:
                print ""
        elif eventType == "DirCreatedEvent":
            print "create dir"
            srcPath = self.getFilePath(item)
            os.mkdir(self.global_info.client_global_directory + srcPath)
        elif eventType == "DirMovedEvent":
            print "TBD"
            #TBD
        elif eventType == "DirDeletedEvent":
            print "delete dir"
            #DeleteDir
        self.global_info.client_global_file_ignore = ""

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
        return event[event.find("=") + 1: event.find(">")]

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
        self.global_info.client_operator.request_file(srcPath)

    def getEventType(self, event):
        return event[event.find("<") + 1:event.find(": ")]
