__author__ = 'David'
import Queue

class ServerGlobal:
    def __init__(self):
        self.GlobalClientEventQueue = Queue.Queue()
        self.GlobalServerDirectory = "C:\\Users\\David\\Desktop\\ServerFolder\\"
        self.GlobalUserID = '1'
        self.GlobalClientFileIgnore = ""
        self.GlobalCurSrcPath = ""
        self.ServerOperator = None