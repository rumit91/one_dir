__author__ = 'Timur'
import communicator
from threading import Thread
import ClientFileUpdateManager
import threading
import sys

GlobalUser = 'test'
GlobalPass = 'test'
class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


class EventDispatcher(communicator.Messenger):
    def set_num_worker_threads(self, num_worker_threads):
        self.num_worker_threads= num_worker_threads

    def do_work(self, event):
        self.send(event)
        print "sent an event"

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
        my_client_file_update_manager = ClientFileUpdateManager.ClientFileUpdateManager(self.global_info)
        #set up the file dispatcher
        myFileDispatcher = FileDispatcher(target_host_name=self.target_host_name, target_port=self.target_port)
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

"""modification starts here"""
class HandShaker(communicator.Messenger):
#    login_info = 'test'
    def get_input(self):
        print "Type in 'Username Password'"
        self.login_info  = sys.stdin.readline()

    def send_login_info(self):
        self.get_input()
        self.send(self.login_info)
        print "send: " + self.login_info
"""end"""

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
                                                            self.target_comm.file_port,
                                                            self.my_global)
        self.my_handshaker = HandShaker(self.my_comm.host_name,
                                          self.my_comm.gatekeeper_port,
                                          self.target_comm.host_name,
                                          self.target_comm.gatekeeper_port,
                                          self.my_global)

    def run(self):
        self.client_operator_thread_1 = myThread(self.my_file_request_listener)
        self.client_operator_thread_1.start()
        self.client_operator_thread_2 = myThread(self.my_event_dispatcher)
        self.client_operator_thread_2.start()
        self.client_operator_thread_3 = myThread(self.my_handshaker)
        #self.client_operator_thread_3.start()