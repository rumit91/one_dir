__author__ = 'David'
import time
import datetime
import os
from threading import Thread
import Queue


class ServerFileUpdateManager():
    def __init__(self, global_info):
        self.global_info = global_info

    def run(self):
        def worker():
            while True:
                item = self.global_info.server_global_event_queue.get()
                self.process_event_for_updates(item, 1)
                self.global_info.server_global_event_queue.task_done()

        for i in range(1):
            t = Thread(target=worker())
            t.daemon = True
            t.start()

    def process_event_for_updates(self, event, updateID):
        with open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\EventLog.txt", "a") as f:
            f.write("\n" + event)
        eventType = self.getEventType(event)
        #Call Correct Method Depending On Event Tye
        if eventType == "FileCreatedEvent":
            srcPath = self.getServerFilePath(event)
            self.global_info.global_cur_src_path = srcPath
            self.requestFile(srcPath)
        elif eventType == "FileModifiedEvent":
            print "request file"
            srcPath = self.getServerFilePath(event)
            self.global_info.global_cur_src_path = srcPath
            self.requestFile(srcPath)
        elif eventType == "FileMovedEvent":
            print "delete file"
            srcPath = self.getServerFilePathMoved(event)
            os.remove(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath)
        elif eventType == "FileDeletedEvent":
            print "delete file"
            srcPath = self.getServerFilePath(event)
            os.remove(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath)
        elif eventType == "DirCreatedEvent":
            print "create dir"
            srcPath = self.getServerFilePath(event)
            os.mkdir(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath)
        elif eventType == "DirMovedEvent":
            print "TBD"
        #TBD
        elif eventType == "DirDeletedEvent":
            print "delete dir"
            #DeleteDir
            #call Operator.unlock(updateID) when finished

    """
    def test_process_events_for_updates(self, updateID):
        print self.global_info.GlobalClientEventQueue
        for event in self.global_info.GlobalClientEventQueue:
            with open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\EventLog.txt", "a") as f:
                f.write("\n" + event)
            eventType = self.getEventType(event)
            #Call Correct Method Depending On Event Tye
            if eventType == "FileCreatedEvent":
                srcPath = self.getServerFilePath(event)
                open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath, 'a').close()
            elif eventType == "FileModifiedEvent":
                srcPath = self.getServerFilePath(event)
                print "request file"
                file = self.requestFile(srcPath)
                with open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath, "wb") as f:
                    f.write(file)
            elif eventType == "FileMovedEvent":
                srcPath = self.getServerFilePathMoved(event)
                print "delete file"
                os.remove(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath)
            elif eventType == "FileDeletedEvent":
                srcPath = self.getServerFilePath(event)
                print "delete file"
                os.remove(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath)
            elif eventType == "DirCreatedEvent":
                srcPath = self.getServerFilePath(event)
                print "create dir"
                os.mkdir(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath)
            elif eventType == "DirMovedEvent":
                srcPath = self.getServerFilePath(event)
                print "TBD"
                #TBD
            elif eventType == "DirDeletedEvent":
                srcPath = self.getServerFilePath(event)
                print "delete dir"
                #DeleteDir
        self.global_info.GlobalClientEventQueue = []
        #call Operator.unlock(updateID) when finished
	"""

    def getServerFilePath(self, event):
        return event[event.find("=") + 1:-1]

    def getServerFilePathMoved(self, event):
        return event[event.find("=") + 1: event.find(",")]

    def get_events_since_last_update(self, lastupdateptimestamp):
        updateList = []
        eventList = self.get_event_log()
        timestampList = self.get_timestamp_log()
        eventList = eventList[::-1]
        timestampList = timestampList[::-1]
        eventNum = 0
        cmptimestamp = datetime.datetime.strptime(lastupdateptimestamp, '%Y-%m-%d %H:%M:%S.%f')
        for timestamp in timestampList:
            curtimestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            if curtimestamp > cmptimestamp:
                updateList.append(eventList[eventNum])
                eventNum = eventNum + 1
            else:
                break
        updateList = updateList[::-1]
        return updateList

    def get_event_log(self):
        eventList = []
        with open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\EventLog.txt", "r") as f:
            for event in f:
                if (event != ""):
                    eventList.append(event[event.find("<") + 1:event.find(">")])
        return eventList

    def get_timestamp_log(self):
        timestampList = []
        count = 0;
        with open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\EventLog.txt", "r") as f:
            for event in f:
                if (event != ""):
                    timestampList.append(event[:event.find("<")])
                    count = count + 1
        return timestampList

    def get_file(self, srcPath):
        try:
            with open(self.global_info.server_global_directory + self.global_info.global_user_id + "\\OneDir\\" + srcPath, 'rb') as f:
                content = f.read()
        except:
            content = ""
        return content

    def requestFile(self, src_path):
        self.global_info.server_operator.request_file(src_path)

    def getEventType(self, event):
        return event[event.find("<") + 1:event.find(": ")]
