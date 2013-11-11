__author__ = 'David'
import Queue
from communicator import CommUnit


class ClientGlobal:
    def __init__(self):
        self.client_global_event_queue = Queue.Queue()
        #self.client_global_directory = ""
        #Timur's Test
        #self.client_global_directory = "C:\\Users\\Timur\\Desktop\\OneDir"
        #David's Test
        #self.client_global_directory = "C:\\Users\\David\\Desktop\\OneDir"
        #Alex's Test
        self.client_global_directory = "Users/AlexQu/Desktop/OneDir"
        self.client_global_file_ignore = ""
        self.client_operator = None
        self.my_host_name = '192.168.56.1'
        self.my_event_port = 12345
        self.my_file_request_port = 12346
        self.my_file_port = 12347
        self.my_comm = CommUnit(self.my_host_name,
                                self.my_event_port,
                                self.my_file_request_port,
                                self.my_file_port)
        self.target_host_name = '192.168.56.1'
        self.target_event_port = 12345
        self.target_file_request_port = 12346
        self.target_file_port = 12347
        self.target_comm = CommUnit(self.target_host_name,
                                    self.target_event_port,
                                    self.target_file_request_port,
                                    self.target_file_port)