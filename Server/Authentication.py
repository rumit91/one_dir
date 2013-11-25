__author__ = 'Timur'
#!/usr/bin/python

import sys
import pickle
from ClientInfoObj import ClientInfoObj
from random import randint
import os


class AuthenticationStrategy:
    def __init__(self, auth_helper):
        self.my_auth_helper = auth_helper

    def authenticate(self):
        return -1

    def get_name(self):
        return "Generic Auth Strategy"

    def get_user_database(self):
        user_database = {}
        try:
            with open('user_database.pkl'):
                print "Found saved user database"
                user_database = pickle.load(open('user_database.pkl', 'rb'))
        except IOError:
            print "No previous user database was found"
        return user_database


class LoginStrategy(AuthenticationStrategy):
    def authenticate(self):
        return self.match_passwd()

    def match_passwd(self):
        self.my_auth_helper.my_global.user_database = self.get_user_database()
        print self.my_auth_helper.my_global.user_database
        try:
            if (self.my_auth_helper.my_global.user_database[self.my_auth_helper.email][0] == self.my_auth_helper.password):
                token = randint(1,65565)
                self.my_auth_helper.auth_result_message = "Authenticated."
                return token
            else:
                self.my_auth_helper.auth_result_message = "Password is incorrect."
                return -1
        except:
            self.my_auth_helper.auth_result_message = "User does not exist."
            return -1

    def get_name(self):
        return "Login Strategy"


class CreateAccountStrategy(AuthenticationStrategy):
    def authenticate(self):
        self.my_auth_helper.my_global.user_database = self.get_user_database()
        if self.my_auth_helper.email in self.my_auth_helper.my_global.user_database:
            self.my_auth_helper.auth_result_message = "User already exists."
            print self.my_auth_helper.auth_result_message
        else:
            self.add_new_user_to_database()
            self.pickle_user_database()
            self.allocate_space_for_new_user()
            token = randint(1, 65565)
            self.my_auth_helper.auth_result_message = "New User Created."
            print self.my_auth_helper.auth_result_message
            return token
        return -1

    def pickle_user_database(self):
        output = open('user_database.pkl', 'wb')
        pickle.dump(self.my_auth_helper.my_global.user_database, output)

    def add_new_user_to_database(self):
        #could fail after deleting 10 users...
        new_user_id = len(self.my_auth_helper.my_global.user_database)+10
        password_id_tuple = (self.my_auth_helper.password, new_user_id)
        self.my_auth_helper.my_global.user_database[self.my_auth_helper.email] = password_id_tuple
        self.my_auth_helper.user_id = new_user_id

    def allocate_space_for_new_user(self):
        folder_path = self.my_auth_helper.my_global.server_global_directory + "\\" + str(self.my_auth_helper.user_id)
        os.mkdir(folder_path)
        os.mkdir(folder_path + "\\OneDir")
        event_log = open(folder_path + "\\" + 'EventLog.txt', 'wb')
        event_log.close()

    def get_name(self):
        return "Create Account Strategy"


class AuthenticationHelper:
    def __init__(self, server_global, message, user_hostname):
        self.my_global = server_global
        message = message.split("|")
        self.action = int(message[0])
        self.email = message[1]
        self.password = message[2]
        self.user_hostname = user_hostname
        self.user_id = -1
        self.user_token = -1
        self.auth_result_message = ""

    def authenticate(self):
        self.acquire_token()
        if self.user_token != -1:
            self.acquire_user_id()
            self.create_client_info_object()

    def acquire_token(self):
        my_strategy = AuthenticationStrategy(self)
        if int(self.action) == 0:
            my_strategy = LoginStrategy(self)
        elif int(self.action) == 1:
            my_strategy = CreateAccountStrategy(self)
        #print my_strategy.get_name()
        self.user_token = my_strategy.authenticate()

    def acquire_user_id(self):
        self.user_id = self.my_global.user_database[self.email][1]

    def create_client_info_object(self):
        client = ClientInfoObj(self.user_id, self.user_hostname)
        self.my_global.active_user_directory[str(self.user_token)] = client

    def print_out(self):
        print "AuthHelper - action: {0} - email: {1} - password: {2}".format(self.action, self.email, self.password)

"""
    def createUser(self,login,passwd):
        saveActiveUser = ActiveUser()
        self.my_ClientInfo = ClientInfoObj
        # read in csv file to check for unique user_id, return False if user_id exists
        tmp = False
        with open('info.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            handle.close()
            if reader.has_key(login):
                return '#'
            else:
                tmp = True
        if tmp == True:
            with open('info.pickle','wb') as handle:
                handle.close()
                reader[login] = passwd
                pickle.dump(reader,handle)
                token = randint(1,65565)
                saveActiveUser.ActiveUserDirectory[token] = self.my_ClientInfo
                return token.to_s()
                ## return True if user created
"""

