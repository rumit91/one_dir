__author__ = 'David'
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
from GlobalCommunicationNetwork import GlobalCommunicationNetwork

class DirectoryWatcherEventHandler(FileSystemEventHandler):
    def __init__(self, observer, Global):
        self.observer = observer
        self.Global = Global

    def on_any_event(self, event):
        #Event Handler Ignores DirModifiedEvents
        if event.src_path == self.Global.GlobalClientFileIgnore:
            return
        if event.event_type == "modified" and event.is_directory == True:
            return
        if event.event_type == "moved" and event.is_directory == True:
            #Special Directory Moved Handling Subroutine
            return
        newEvent = str(event).replace(self.Global.GlobalClientDirectory,"")
        newEvent = str(datetime.datetime.now()) + newEvent
        self.Global.GlobalClientEventQueue.append(newEvent)
        print newEvent
        #print self.eventQueue
        #Future: Make Directory Event Queue Optimizer - Might actually be a different construct and will be called
        #when dispatcher is used

class DirectoryWatcher():
    def __init__(self, Global):
        self.Global = Global

    def run(self):
        observer = Observer()
        event_handler = DirectoryWatcherEventHandler(observer,self.Global)
        observer.schedule(event_handler, path=self.Global.GlobalClientDirectory, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


