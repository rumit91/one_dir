__author__ = 'Timur'
import ClientGlobal
import DirectoryWatcher
import ClientOperator
import socket
import os
import threading
import sys
import datetime
import time
import pickle


class myThread(threading.Thread):
    def __init__(self, run_object):
        threading.Thread.__init__(self)
        self.run_object = run_object

    def run(self):
        print "Starting"
        self.run_object.run()
        print "Ending"

# on start up:
# get the user's ip address
# if a pickled file exists for ClientGlobal
#   import ClientGlobal
#   change the local ip address
#   if user credentials are stored
#       automatically log the user in and store the token
#       request an update from the server
#   else
#       ask if logging in
#           ask for user credentials
#           ask if they should be saved
#       elif creating a new account
#           ask for email and password twice
#           ask if credentials should be saved
#           create a new account


def get_client_global():
    client_global = ClientGlobal.ClientGlobal()
    try:
        with open('client_global.pkl'):
            print "Found saved user data"
            client_global = pickle.load(open('client_global.pkl', 'rb'))
    except IOError:
        print "No previous user data was found"
    return client_global


def pickle_client_global(client_global):
    output = open('client_global.pkl', 'wb')
    pickle.dump(client_global, output)


client_global = get_client_global()
client_global.my_host_name = socket.gethostbyname(socket.getfqdn())
client_operator = ClientOperator.ClientOperator(client_global.my_comm, client_global.target_comm, client_global)
client_global.client_operator = client_operator
client_operator.run()
client_directory_watcher = DirectoryWatcher.DirectoryWatcher(client_global)
if(client_global.email == ""):
    action = "-1"
    email = ''
    password = ''
    while(action == "-1"):
        action = raw_input("What would you like to do? (0 - login, 1 - create a new account): ")
        if(action == "0"):
            print "Logging in:"
            email = raw_input("Please enter your email address: ")
            password = raw_input("Please enter your password: ")
            save = ""
            while(save == ""):
                save = raw_input("Would you like your credentials to be saved (y or n): ")
                if(save == "y"):
                    client_global.email = email
                    client_global.password = password
                elif(save == "n"):
                    print "Please note that you will have to login again in the future."
                else:
                    save = ""
                    print "Unable to process your input, please try again."
        elif(action == "1"):
            print "Creating a new account:"
            email = raw_input("Please enter an email address: ")
            password = 'x'
            password_confirmation = 'y'
            while(password != password_confirmation):
                password = raw_input("Please enter a password: ")
                password_confirmation = raw_input("Please enter the password again: ")
                if(password != password_confirmation):
                    print "Sorry your passwords did not match. Please try again."
        else:
            action = "-1"
            print "Unable to process your input, please try again."

    client_operator.set_auth_message(action, email, password)
    client_operator.my_authentication_dispatcher.authenticate()
    #save the current global state
    pickle_client_global(client_global)
else:
    action = "-1"
    while(action == "-1"):
        action = raw_input("Hi {0}! What would you like to do? (0 - continue, 1 - logout): ".format(client_global.email))
        if(action == "0"):
            #log in automatically
            client_operator.set_auth_message(0, client_global.email, client_global.password)
            client_operator.my_authentication_dispatcher.authenticate()
            #save the current global state
            pickle_client_global(client_global)
        elif(action == "1"):
            os.remove("client_global.pkl")
            print "The local user information was deleted. Please restart the application"
            sys.exit(0)         # currently does not terminate the program because of multi threading
        else:
            action = "-1"
            print "Unable to process your input, please try again."

while(client_global.token == None):
    #Do Nothing - Waits for token to be returned
    continue

print 'about to request updates from server'
client_operator.my_update_dispatcher.set_token(client_global.token)
client_operator.my_update_dispatcher.set_timestamp("2013-11-16 16:36:39.753000")
client_operator.my_update_dispatcher.request_update()
print "WAITING 10 SECONDS TO START DIRECTORY WATCHER AFTER UPDATING ENDS"
time.sleep(10)

print 'about to run the directoryWatcher'
client_directory_watcher_thread = myThread(client_directory_watcher)
client_directory_watcher_thread.start()


