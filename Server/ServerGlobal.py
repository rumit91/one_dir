__author__ = 'David'
import Queue
from communicator import CommUnit


class ServerGlobal:
    def __init__(self):
        self.server_global_event_queue = Queue.Queue()
        #self.server_global_directory = "D:\\dev\\one_dir\\one_dirs\\"
        #Timur's Test
        #self.server_global_directory = "C:\\Users\\Timur\\Desktop\\ServerFolder\\"
        #David's Test
        #self.server_global_directory = "C:\\Users\\David\\Desktop\\ServerFolder\\"
        #Alex's Test
        self.client_global_directory = "Users/AlexQu/Desktop/ServerFolder"
        self.global_user_id = '1'
        self.global_file_ignore = ""
        self.global_cur_src_path = ''
        self.server_operator = None
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