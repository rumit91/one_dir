__author__ = 'David'
import Queue
from communicator import CommUnit


class ClientGlobal:
    def __init__(self):
        self.client_global_event_queue = Queue.Queue()
        self.client_global_update_queue = Queue.Queue()
        self.client_global_share_queue = Queue.Queue()
        #self.client_global_directory = ""
        #Timur's Test
        #self.client_global_directory = "C:\\Users\\Timur\\Desktop\\OneDir"
        #David's Test
        self.client_global_directory = "C:\\Users\\David\\Desktop\\OneDir"
        #David's Test 2
        #self.client_global_directory = "C:\Users\David\Desktop\OneDir1"
        #Alex's Test
        #self.client_global_directory = "C:\\Users\\Chilaxus\\Desktop\\OneDir"
        #self.client_global_directory = "C:\\Users\\Alex Qu\\Desktop\\OneDir"
        self.client_global_directory_actual = self.client_global_directory
        self.email = ""
        self.password = ""
        self.temp_email = ""
        self.temp_password = ""
        self.sync_on = True
        self.updating = False
        self.client_global_file_ignore = ''
        self.global_cur_src_path = ''
        self.client_operator = None
        self.token = None
        self.auth_result_message = ''
        self.my_host_name = '192.168.56.1'
        self.my_event_port = 12345
        self.my_file_request_port = 12346
        self.my_file_port = 12347
        self.my_authentication_port = 12348
        self.my_update_port = 12349
        self.my_comm = CommUnit(self.my_host_name,
                                self.my_event_port,
                                self.my_file_request_port,
                                self.my_file_port,
                                self.my_authentication_port,
                                self.my_update_port)
        #self.target_host_name = '192.168.56.1'
        self.target_host_name = ''
        self.target_event_port = 22345
        self.target_file_request_port = 22346
        self.target_file_port = 22347
        self.target_authentication_port = 22348
        self.target_comm = CommUnit(self.target_host_name,
                                    self.target_event_port,
                                    self.target_file_request_port,
                                    self.target_file_port,
                                    self.target_authentication_port)
        self.lastupdate = "2010-11-18 12:29:15.998000"

    def __getstate__(self):
        odict = self.__dict__.copy()    # copy the dict since we change it
        del odict['token']
        del odict['auth_result_message']
        del odict['my_comm']
        del odict['target_comm']
        del odict['client_operator']
        del odict['client_global_event_queue']
        del odict['client_global_update_queue']
        del odict['client_global_share_queue']
        del odict['temp_email']
        del odict['temp_password']
        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        self.client_global_event_queue = Queue.Queue()
        self.client_global_update_queue = Queue.Queue()
        self.client_global_share_queue = Queue.Queue()
        self.token = None
        self.sync_on = True
        self.updating = False
        self.auth_result_message = ''
        self.my_comm = CommUnit(self.my_host_name,
                                self.my_event_port,
                                self.my_file_request_port,
                                self.my_file_port,
                                self.my_authentication_port,
                                self.my_update_port)
        self.target_comm = CommUnit(self.target_host_name,
                                    self.target_event_port,
                                    self.target_file_request_port,
                                    self.target_file_port,
                                    self.target_authentication_port)
        self.client_operator = None
        self.temp_email = self.email
        self.temp_password = self.password