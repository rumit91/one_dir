__author__ = 'Timur'
import ClientGlobal
import DirectoryWatcher
import ClientOperator
import socket
import threading


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"

client_global = ClientGlobal.ClientGlobal()
client_operator = ClientOperator.ClientOperator(client_global.my_comm, client_global.target_comm, client_global)
client_global.client_operator = client_operator
client_directory_watcher = DirectoryWatcher.DirectoryWatcher(client_global)
sys.arg.pop(0)
auth_message = sys.arg.split('|')
auth_messenger = Communicator.Messenger(client_global.target_hostname,client_global.target_gatekeeper_port)
auth_messenger.send(auth_message)

print 'about to run the directoryWatcher'
client_directory_watcher_thread = myThread(client_directory_watcher)
client_directory_watcher_thread.start()
print 'about to run the clientOperator'
client_operator.run()


