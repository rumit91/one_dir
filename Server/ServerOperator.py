__author__ = 'Timur'
import communicator
import threading
import GateKeeper

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
                          self.global_info.global_user_id +
                          "\\OneDir\\" +
                          self.global_info.global_cur_src_path,
                  "wb") as f:
            f.write(message)

    def run(self):
        self.setup()
        self.spin()

class HandShakerListener(communicator.Receiver):
    def get_login_info(self,message):
        print 'Getting message: '+message
        self.user_info = message
        return self.user_info

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
        self.my_handshaker_listener = HandShakerListener(self.my_comm.host_name,
                                          self.my_comm.gatekeeper_port,
                                          self.target_comm.host_name,
                                          self.target_comm.gatekeeper_port,
                                          self.my_global)
    def run(self):
        self.server_operator_thread_1 = myThread(self.my_file_listener)
        self.server_operator_thread_1.start()
        self.server_operator_thread_2 = myThread(self.my_event_listener)
        self.server_operator_thread_2.start()
        self.server_operator_thread_3 = myThread(self.my_handshaker_listener)
        self.server_operator_thread_3.start()

    def request_file(self, src_path):
        print self.target_comm.host_name
        my_file_request_dispatcher = FileRequestDispatcher(target_host_name=self.target_comm.host_name,
                                                           target_port=self.target_comm.file_request_port)
        my_file_request_dispatcher.set_file_path(src_path)
        my_file_request_dispatcher.request_file()
        print "Requesting File"

    def initiateGateKeeper(self):
        my_gatekeeper = GateKeeper.Authentication()
        #below will return the token number
        print "token number is: ",my_gatekeeper.run("wrong login")
        print "token number is: ",my_gatekeeper.run("alex Qu")


        """send token back to the client"""
