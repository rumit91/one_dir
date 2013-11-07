__author__ = 'Timur'
import ServerFileUpdateManager
import ServerGlobal
import ServerOperator
import threading


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


server_global = ServerGlobal.ServerGlobal()
server_operator = ServerOperator.ServerOperator(server_global.my_comm, server_global.target_comm, server_global)
server_global.server_operator = server_operator
server_file_update_manager = ServerFileUpdateManager.ServerFileUpdateManager(server_global)
print 'about to run the server_operator'
server_operator.run()
print 'about to run the server_file_update_manager'
serverFileUpdateManagerThread = myThread(server_file_update_manager)
serverFileUpdateManagerThread.start()

