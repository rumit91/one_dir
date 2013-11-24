__author__ = 'Timur'
import communicator
from threading import Thread
from ClientFileUpdateManager import ClientFileUpdateManager
import threading
import sys


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        #print "Starting"
        self.run_object.run()
        #print "Ending"


class EventDispatcher(communicator.Messenger):
    def set_num_worker_threads(self, num_worker_threads):
        self.num_worker_threads= num_worker_threads

    def do_work(self, event):
        self.send(str(self.global_info.token) + "|" + event)
        print "sent an token + event"

    def run(self):
        def worker():
            while True:
                item = self.global_info.client_global_event_queue.get()
                self.do_work(item)
                self.global_info.client_global_event_queue.task_done()

        self.set_num_worker_threads(1)
        for i in range(self.num_worker_threads):
            t = Thread(target=worker())
            t.daemon = True
            t.start()


class FileRequestListener(communicator.Receiver):
    def dispatch(self, message):
        print ["New File Request: ", message]
        my_client_file_update_manager = ClientFileUpdateManager(self.global_info)
        #set up the file dispatcher
        myFileDispatcher = FileDispatcher(target_host_name=self.target_host_name,
        target_port=self.global_info.target_comm.file_port)
        myFileDispatcher.set_file_path(message)
        myFileDispatcher.set_file_update_manager(my_client_file_update_manager)
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

    def get_file(self):
        my_file = self.my_file_update_manager.get_file(self.my_file_path)
        self.send(my_file)


class AuthenticationDispatcher(communicator.Messenger):
    def set_action(self, action):
        self.action = action

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def set_message(self, auth_message):
        self.action = auth_message.action
        self.email = auth_message.email
        self.password = auth_message.password

    def authenticate(self):
        my_message = str(self.action) + "|" + self.email + "|" + self.password
        self.send(my_message)


class AuthenticationListener(communicator.Receiver):
    def dispatch(self, message):
        message = message.split("|")
        self.global_info.token = int(message[0])
        self.global_info.auth_result_message = message[1]

    def run(self):
        self.setup()
        self.spin()


class UpdateDispatcher(communicator.Messenger):
    def set_token(self, token):
        self.token = token

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def request_update(self):
        my_message = str(self.token) + "|~UPDATE~|" + str(self.timestamp)
        self.send(my_message)


class UpdateListener(communicator.Receiver):
    def dispatch(self,message):
        print message
        updateList = message.split("|")
        for event in updateList:
            self.global_info.client_global_update_queue.put(event)
        CFUM = ClientFileUpdateManager(self.global_info)
        CFUM.run()

    def run(self):
        self.setup()
        self.spin()


class FileRequestDispatcher(communicator.Messenger):
    def set_file_path(self, file_path):
        self.my_file_path = file_path

    def request_file(self):
        self.send(str(self.global_info.token) + "|" + self.my_file_path)


class FileListener(communicator.Receiver):
    def dispatch(self, message):
        print ["New File: ", message]
        print "WRITING"
        self.write_file(message)
        print "finished"

    def write_file(self, message):
        print message
        with open(self.global_info.client_global_directory + self.global_info.global_cur_src_path,
                  "wb") as f:
            f.write(message)

    def run(self):
        self.setup()
        self.spin()

class ClientOperator:
    def __init__(self, my_comm, target_comm, global_info):
        self.my_comm = my_comm
        self.target_comm = target_comm
        self.my_global = global_info
        self.my_event_dispatcher = EventDispatcher(target_host_name=self.target_comm.host_name,
                                                   target_port=self.target_comm.event_port,
                                                   global_info=self.my_global)
        self.my_file_request_listener = FileRequestListener(self.my_comm.host_name,
                                                            self.my_comm.file_request_port,
                                                            self.target_comm.host_name,
                                                            self.target_comm.file_request_port,
                                                            self.my_global)
        self.my_authentication_listener = AuthenticationListener(self.my_comm.host_name,
                                                                 self.my_comm.authentication_port,
                                                                 self.target_comm.host_name,
                                                                 self.target_comm.authentication_port,
                                                                 self.my_global)
        self.my_authentication_dispatcher = AuthenticationDispatcher(self.my_comm.host_name,
                                                                     self.my_comm.authentication_port,
                                                                     self.target_comm.host_name,
                                                                     self.target_comm.authentication_port,
                                                                     self.my_global)
        self.my_update_listener = UpdateListener(my_host_name = self.my_comm.host_name,
                                                 my_port = self.my_comm.update_port,
                                                 target_port = self.target_comm.host_name,
                                                 global_info = self.my_global)
        self.my_update_dispatcher = UpdateDispatcher(self.my_comm.host_name,
                                                     self.my_comm.event_port,
                                                     self.target_comm.host_name,
                                                     self.target_comm.event_port,
                                                     self.my_global)
        self.my_file_listener = FileListener(self.my_comm.host_name,
                                             self.my_comm.file_port,
                                             self.target_comm.host_name,
                                             self.target_comm.file_port,
                                             self.my_global)

    def run(self):
        print "Starting the file_request_listener"
        self.client_operator_thread_1 = myThread(self.my_file_request_listener)
        self.client_operator_thread_1.start()
        print "Starting the event_dispatcher"
        self.client_operator_thread_2 = myThread(self.my_event_dispatcher)
        self.client_operator_thread_2.start()
        print "Starting the authentication_listener"
        self.client_operator_thread_3 = myThread(self.my_authentication_listener)
        self.client_operator_thread_3.start()
        print "Starting the update_listener"
        self.client_operator_thread_4 = myThread(self.my_update_listener)
        self.client_operator_thread_4.start()
        print "Starting the file_listener"
        self.client_operator_thread_5 = myThread(self.my_file_listener)
        self.client_operator_thread_5.start()

    def set_auth_message_with_pieces(self, action, email, password):
        self.my_authentication_dispatcher.set_action(action)
        self.my_authentication_dispatcher.set_email(email)
        self.my_authentication_dispatcher.set_password(password)

    def set_auth_message_with_full_message(self, auth_message):
        self.my_authentication_dispatcher.set_message(auth_message)

    def request_file(self, src_path):
        my_file_request_dispatcher = FileRequestDispatcher(target_host_name=self.my_global.target_host_name,
                                                           target_port=self.target_comm.file_request_port,
                                                           global_info = self.my_global)
        my_file_request_dispatcher.set_file_path(src_path)
        my_file_request_dispatcher.request_file()
        print "Requesting File From Server"