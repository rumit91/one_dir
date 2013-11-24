__author__ = 'AlexQu'
#!/usr/bin/python

import sys
import pickle
from ClientInfoObj import ClientInfoObj
from random import randint


class AuthenticationStrategy:
    def __init__(self, auth_helper):
        self.my_auth_helper = auth_helper

    def authenticate(self):
        return -1

    def get_name(self):
        return "Generic Auth Strategy"


class LoginStrategy(AuthenticationStrategy):
    def authenticate(self):
        return self.match_passwd()

    def match_passwd(self):
        self.my_auth_helper.my_global.user_database = self.get_user_database()
        print self.my_auth_helper.my_global.user_database
        try:
            if (self.my_auth_helper.my_global.user_database[self.my_auth_helper.email][0] == self.my_auth_helper.password):
                token = randint(1,65565)
                self.my_auth_helper.auth_message = "Authenticated"
                return token
            else:
                return -1
        except:
            return -1

    def get_name(self):
        return "Login Strategy"

    def get_user_database(self):
        user_database = {}
        try:
            with open('./Server/user_database.pkl'):
                print "Found saved user database"
                user_database = pickle.load(open('./Server/user_database.pkl', 'rb'))
        except IOError:
            print "No previous user database was found"
        return user_database


class CreateAccountStrategy(AuthenticationStrategy):
    def authenticate(self):
        return -1

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
            self.auth_result_message = "Authenticated."
        else:
            self.auth_result_message = "Unable to authenticate."

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

