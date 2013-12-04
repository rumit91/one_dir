__author__ = 'Timur'
import ServerFileUpdateManager
import LinuxServerFileUpdateManager
import ServerGlobal
import ServerOperator
import threading
import os
import pickle
import socket
from sys import platform as _platform


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"


def create_user_database():
    user_database = {'david': ['pass', 1,0], 'david1': ['pass2', 2,0]}
    output = open('user_database.pkl', 'wb')
    pickle.dump(user_database, output)
    output.close()


def create_user_connection_log():
    ActiveUserLog = {'user' : (('address','timestamp'))}
    output = open('user_connection_log.pkl', 'wb')
    pickle.dump(ActiveUserLog, output)
    output.close()


def ask_to_reset():
    action = "-1"
    while action == "-1":
        action = raw_input("Would you like to reset the server? (y or n): ")
        if action == 'y':
            print "Resetting..."
            try:
                os.remove("user_database.pkl")
                print "Deleted the user database"
            except:
                print "Database is already removed"
            try:
                os.remove("user_connection_log.pkl")
                print "Deleted the user connection log"
            except:
                print "User connection log is already removed"
            create_user_database()
            create_user_connection_log()
            print "Reset complete."
        elif action == 'n':
            print "Continuing..."
        else:
            action = "-1"
            print "Unable to process your input, please try again."


def confirm_host_name(server_global):
    action = "-1"
    while action == "-1":
        action = raw_input("The current server ip address is {0}. Is this correct? (y or n): ".format(server_global.my_host_name))
        if action == 'y':
            print "Continuing..."
        elif action == 'n':
            server_global.my_host_name = raw_input("Please enter the server ip address: ")
        else:
            action = '-1'
            print "Unable to process your input, please try again."
    server_global.my_comm.host_name = server_global.my_host_name


def confirm_server_directory(server_global):
    action = "-1"
    while action == "-1":
        action = raw_input("The current directory is {0}. Is this correct? (y or n): ".format(server_global.server_global_directory))
        if action == 'y':
            print "Continuing..."
        elif action == 'n':
            server_global.server_global_directory = raw_input("Please enter the server directory: ")
            print "Set the server directory to {0}".format(server_global.server_global_directory)
        else:
            action = '-1'
            print "Unable to process your input, please try again."


ask_to_reset()
server_global = ServerGlobal.ServerGlobal()
confirm_host_name(server_global)
confirm_server_directory(server_global)
server_operator = ServerOperator.ServerOperator(server_global.my_comm, server_global.target_comm, server_global)
server_global.server_operator = server_operator

if _platform == "linux" or _platform == "linux2":
    server_file_update_manager = LinuxServerFileUpdateManager.LinuxServerFileUpdateManager(server_global)
elif _platform == "win32":
    server_file_update_manager = ServerFileUpdateManager.ServerFileUpdateManager(server_global)
#For use of testing eventLog parsing
#print server_file_update_manager.get_events_since_last_update("2013-11-10 11:58:48.335000")
print 'about to run the server_operator'
server_operator.run()

print 'about to run the server_file_update_manager'
serverFileUpdateManagerThread = myThread(server_file_update_manager)
serverFileUpdateManagerThread.start()

