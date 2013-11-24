__author__ = 'Timur'
import communicator
import threading
from Authentication import AuthenticationHelper
from ClientInfoObj import ClientInfoObj
from ServerFileUpdateManager import ServerFileUpdateManager
import socket

#GlobalMessage = ''
class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


class EventListener(communicator.Receiver):
    def dispatch(self, message):
        print ["New Event: ", message]
        self.global_info.server_global_event_queue.put(message)

    def run(self):
        self.setup()
        self.spin()


class FileRequestDispatcher(communicator.Messenger):
    def set_file_path(self, file_path):
        self.my_file_path = file_path

    def request_file(self):
        self.send(self.my_file_path)


class FileListener(communicator.Receiver):
    def dispatch(self, message):
        print ["New File: ", message]
        print "WRITING"
        self.write_file(message)
        print "finished"

    def write_file(self, message):
        with open(self.global_info.server_global_directory +
                          self.global_info.global_cur_user_id +
                          "\\OneDir\\" +
                          self.global_info.global_cur_src_path,
                  "wb") as f:
            f.write(message)

    def run(self):
        self.setup()
        self.spin()

class FileRequestListener(communicator.Receiver):
    def dispatch(self, message):
        print "New File Request: " + message
        my_server_file_update_manager = ServerFileUpdateManager(self.global_info)
        #set up the file dispatcher
        message = message.split("|")
        myFileDispatcher = FileDispatcher(target_host_name=self.global_info.active_user_directory[message[0]].host_name,
        target_port=self.global_info.target_comm.file_port)
        myFileDispatcher.set_file_path(message[1])
        myFileDispatcher.set_token(message[0])
        myFileDispatcher.set_file_update_manager(my_server_file_update_manager)
        #run the file dispatcher
        myFileDispatcher.get_file()

    def run(self):
        self.setup()
        self.spin()


class FileDispatcher(communicator.Messenger):
    def set_file_update_manager(self, file_update_manager):
        self.my_file_update_manager = file_update_manager

    def set_file_path(self, file_path):
        self.my_file_path = file_path

    def set_token(self, token):
        self.token = token

    def get_file(self):
        my_file = self.my_file_update_manager.get_file(self.token, self.my_file_path)
        self.send(my_file)


class AuthenticationListener(communicator.Receiver):
    def dispatch(self, message):
        print "New Auth Request: " + message
        #message = message.split("|")
        my_authenticator = AuthenticationHelper(self.global_info, message, self.addr[0])
        my_authenticator.print_out()
        my_authenticator.authenticate()
        if my_authenticator.user_token != -1:
            print "Authenticated"
            print "User Token: " + str(my_authenticator.user_token)
            #add the newly authenticated user to the active_user_directory
            client = ClientInfoObj(my_authenticator.user_id, self.addr[0])
            self.global_info.active_user_directory[my_authenticator.user_token] = client
            print self.global_info.active_user_directory[my_authenticator.user_token].print_out()
        else:
            print "Unable to Authenticate"
        #TO-DO: consider creating a dispatcher object in the ServerOperator
        myAuthenticationDispatcher = communicator.Messenger(target_host_name=self.target_host_name,
                                                            target_port=self.global_info.target_comm.authentication_port)
        myAuthenticationDispatcher.send(str(my_authenticator.user_token) + "|" + my_authenticator.auth_result_message)

    def run(self):
        self.setup()
        self.spin()


class ServerOperator:
    GlobalMessage = ''

    def __init__(self, my_comm, target_comm, global_info):
        self.my_comm = my_comm
        self.target_comm = target_comm
        self.my_global = global_info
        #self.my_file_request_dispatcher = FileRequestDispatcher(target_host_name=self.target_comm.host_name,
        #                                                        target_port=self.target_comm.event_port,
        #                                                        global_info=self.my_global)
        self.my_file_listener = FileListener(self.my_comm.host_name,
                                             self.my_comm.file_port,
                                             self.target_comm.host_name,
                                             self.target_comm.file_port,
                                             self.my_global)
        self.my_event_listener = EventListener(self.my_comm.host_name,
                                               self.my_comm.event_port,
                                               self.target_comm.host_name,
                                               self.target_comm.event_port,
                                               self.my_global)
        self.my_authentication_listener = AuthenticationListener(self.my_comm.host_name,
                                          self.my_comm.authentication_port,
                                          self.target_comm.host_name,
                                          self.target_comm.authentication_port,
                                          self.my_global)

        self.my_file_request_listener = FileRequestListener(self.my_comm.host_name,
                                               self.my_comm.file_request_port,
                                               self.target_comm.host_name,
                                               self.target_comm.file_request_port,
                                               self.my_global)

    def run(self):
        self.server_operator_thread_1 = myThread(self.my_file_listener)
        self.server_operator_thread_1.start()
        self.server_operator_thread_2 = myThread(self.my_event_listener)
        self.server_operator_thread_2.start()
        self.server_operator_thread_3 = myThread(self.my_authentication_listener)
        self.server_operator_thread_3.start()
        self.server_operator_thread_3 = myThread(self.my_file_request_listener)
        self.server_operator_thread_3.start()

    def request_file(self, src_path, token):
        my_file_request_dispatcher = FileRequestDispatcher(target_host_name=self.my_global.active_user_directory[token].host_name,
                                                           target_port=self.target_comm.file_request_port)
        my_file_request_dispatcher.set_file_path(src_path)
        my_file_request_dispatcher.request_file()
        print "Requesting File"

    def send_update_list(self, updateListString, token):
        my_update_dispatcher = communicator.Messenger(target_host_name=self.my_global.active_user_directory[token].host_name,
                                                           target_port=self.target_comm.update_port)
        my_update_dispatcher.send(updateListString)
        print "Sending Update List"


