__author__ = 'Timur'
import communicator
import threading


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
        with open(self.global_info.GlobalServerDirectory +
                          self.global_info.GlobalUserID +
                          "\\OneDir\\" +
                          self.global_info.GlobalCurSrcPath,
                  "wb") as f:
            f.write(message)

    def run(self):
        self.setup()
        self.spin()


class ServerOperator:
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

    def run(self):
        self.server_operator_thread_1 = myThread(self.my_file_listener)
        self.server_operator_thread_1.start()
        self.server_operator_thread_2 = myThread(self.my_event_listener)
        self.server_operator_thread_2.start()