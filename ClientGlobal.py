__author__ = 'David'
import Queue
class ClientGlobal:
    def __init__(self):
        self.GlobalClientEventQueue = Queue.Queue()
        self.GlobalClientDirectory = "C:\\Users\\David\\Desktop\\OneDir\\"
        self.GlobalClientFileIgnore = ""
        self.ClientOperator = None