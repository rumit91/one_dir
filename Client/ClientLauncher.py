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


class auth_message:
    def __init__(self):
        self.action = "-1"
        self.email = ""
        self.password = ""
        self.new_password = ""

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


def manual_log_in(client_global, my_auth_message):
    print "Logging in:"
    my_auth_message.email = raw_input("Please enter your email address: ")
    my_auth_message.password = raw_input("Please enter your password: ")
    save = ""
    while save == "":
        save = raw_input("Would you like your credentials to be saved (y or n): ")
        if save == "y":
            client_global.email = my_auth_message.email
            client_global.password = my_auth_message.password
            client_global.temp_email = my_auth_message.email
            client_global.temp_password = my_auth_message.password
        elif save == "n":
            print "Please note that you will have to login again in the future."
            client_global.temp_email = my_auth_message.email
            client_global.temp_password = my_auth_message.password
        else:
            save = ""
            print "Unable to process your input, please try again."
    send_auth_message_to_server(my_auth_message)


def automatic_log_in(client_global):
    my_auth_message = auth_message()
    my_auth_message.action = 0
    my_auth_message.email = client_global.email
    my_auth_message.password = client_global.password
    send_auth_message_to_server(my_auth_message)


def create_new_account(client_global, my_auth_message):
    print "Creating a new account:"
    my_auth_message.email = raw_input("Please enter an email address: ")
    my_auth_message.password = 'x'
    password_confirmation = 'y'
    while my_auth_message.password != password_confirmation:
        my_auth_message.password = raw_input("Please enter a password: ")
        password_confirmation = raw_input("Please enter the password again: ")
        if my_auth_message.password != password_confirmation:
            print "Sorry your passwords did not match. Please try again."
    send_auth_message_to_server(my_auth_message)


def send_auth_message_to_server(my_auth_message):
    print("Contacting server for authentication...")
    # TO-DO: Might want to consider adding the client_operator as a parameter to this method
    client_operator.set_auth_message_with_full_message(my_auth_message)
    client_operator.my_authentication_dispatcher.authenticate()


def process_user_input(client_global):
    if client_global.email == "":
        my_auth_message = auth_message()
        while my_auth_message.action == "-1":
            my_auth_message.action = raw_input("What would you like to do? (0 - login, 1 - create a new account): ")
            if my_auth_message.action == "0":
                manual_log_in(client_global, my_auth_message)
            elif my_auth_message.action == "1":
                create_new_account(client_global, my_auth_message)
            else:
                my_auth_message.action = "-1"
                print "Unable to process your input, please try again."
        #save the current global state
        pickle_client_global(client_global)
    else:
        action = "-1"
        while action == "-1":
            action = raw_input("Hi {0}! What would you like to do? (0 - continue, 1 - logout): ".format(client_global.email))
            if action == "0":
                automatic_log_in(client_global)
                #save the current global state
                pickle_client_global(client_global)
            elif action == "1":
                os.remove("client_global.pkl")
                print "The local user information was deleted. Please restart the application"
                sys.exit(0)         # currently does not terminate the program because of multi threading
            else:
                action = "-1"
                print "Unable to process your input, please try again."


def toggle_sync(client_global):
    print "About to toggle sync"
    if client_global.sync_on:
        #send a message to turn sync off
        print "Turning sync off"
        client_global.sync_on = False
    else:
        print "Turning sync on"
        client_global.sync_on = True


def request_update(client_global, timestamp):
    client_operator.my_update_dispatcher.set_token(client_global.token)
    client_operator.my_update_dispatcher.set_timestamp(timestamp)
    client_operator.my_update_dispatcher.request_update()


def request_share(client_global, sharetoken, directory):
    client_global.sync_on = False
    client_global.global_client_directory = directory
    client_operator.my_share_dispatcher.set_token(client_global.token)
    client_operator.my_share_dispatcher.set_sharetoken(sharetoken)
    client_operator.my_share_dispatcher.request_share()


def request_password_change(client_global, current_password, new_password):
    password_message = auth_message()
    password_message.action = 2
    password_message.email = client_global.temp_email
    password_message.password = current_password
    password_message.new_password = new_password
    print("Contacting server for a password change...")
    # TO-DO: Might want to consider adding the client_operator as a parameter to this method
    client_operator.set_auth_message_with_full_message(password_message)
    client_operator.my_authentication_dispatcher.authenticate()


def change_password(client_global):
    client_global.token = None
    current_password = raw_input("Please enter your current password: ")
    new_password = raw_input('Please enter the new password: ')
    request_password_change(client_global, current_password, new_password)
    while client_global.token == None or client_global.token == -1:
        if client_global.token != None and client_global.token == -1:
            print "{0} Please try again.".format(client_global.auth_result_message)
            client_global.token = None
            client_global.auth_result_message = ''
            change_password(client_global)



client_global = get_client_global()
#get the ip address automatically - may not work on all machines...
#client_global.my_host_name = socket.gethostbyname(socket.getfqdn())
client_operator = ClientOperator.ClientOperator(client_global.my_comm, client_global.target_comm, client_global)
client_global.client_operator = client_operator
client_operator.run()
client_directory_watcher = DirectoryWatcher.DirectoryWatcher(client_global)

process_user_input(client_global)

while client_global.token == None or client_global.token == -1:
    if client_global.token != None and client_global.token == -1:
        print "{0} Please try again.".format(client_global.auth_result_message)
        client_global.token = None
        client_global.auth_result_message = ''
        process_user_input(client_global)

print '{0} About to request updates from server.'.format(client_global.auth_result_message)
request_update(client_global, "2013-11-16 16:36:39.753000")

#print "WAITING 10 SECONDS TO START DIRECTORY WATCHER AFTER UPDATING ENDS"
#time.sleep(10)

print 'about to run the directoryWatcher'
client_directory_watcher_thread = myThread(client_directory_watcher)
client_directory_watcher_thread.start()

action = "-1"
while True:
    action = raw_input("What would you like to do? (0 - update, 1 - logout, 2 - toggle sync, 3 - change password, 4 - request shared files): ")
    if action == "0":
        #trigger a manual update
        print "Requesting an update..."
        request_update(client_global, str(datetime.datetime.now()))
    elif action == "1":
        #logout
        os.remove("client_global.pkl")
        print "The local user information was deleted. Please restart the application"
        sys.exit(0)         # currently does not terminate the program because of multi threading
    elif action == "2":
        #toggle sync
        toggle_sync(client_global)
    elif action == "3":
        #change password
        change_password(client_global)
    elif action == "4":
        #change password
        sharetoken = raw_input("Please enter the share token given to you: ")
        directory = raw_input("Please enter the directory you would like to save the shared file to: ")
        request_share(client_global, sharetoken, directory)
    else:
        action = "-1"
        print "Unable to process your input, please try again."

