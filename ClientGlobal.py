__author__ = 'David'
import Queue
class ClientGlobal:
    def __init__(self):
        self.GlobalClientEventQueue = Queue.Queue()
        self.GlobalClientDirectory = "D:\\dev\\one_dir\\one_dirc\\"
        self.GlobalClientFileIgnore = ""
        self.ClientOperator = None