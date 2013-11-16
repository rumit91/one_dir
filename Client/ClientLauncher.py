__author__ = 'Timur'
import ClientGlobal
import DirectoryWatcher
import ClientOperator
import socket
import communicator
import threading
import sys
import datetime
import time


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
client_operator.run()
client_directory_watcher = DirectoryWatcher.DirectoryWatcher(client_global)
auth_message = "david|pass"
auth_messenger = communicator.Messenger(target_host_name=client_global.target_host_name,target_port=client_global.target_authentication_port)
auth_messenger.send(auth_message)
while(client_global.token == None):
    #Do Nothing - Waits for token to be returned
    continue

print 'about to request updates from server'
#update_message = client_global.token + "|" + "~UPDATE~" + "|" + str(datetime.datetime.now())
update_message = client_global.token + "|" + "~UPDATE~" + "|" + "2013-11-16 16:36:39.753000"
update_messenger = communicator.Messenger(target_host_name=client_global.target_host_name,target_port=client_global.target_event_port)
update_messenger.send(update_message)
print "WAITING 10 SECONDS TO START DIRECTORY WATCHER AFTER UPDATING ENDS"
time.sleep(10)

print 'about to run the directoryWatcher'
client_directory_watcher_thread = myThread(client_directory_watcher)
client_directory_watcher_thread.start()



