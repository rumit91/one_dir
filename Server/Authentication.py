__author__ = 'AlexQu'
#!/usr/bin/python

import sys
import pickle
from ClientInfoObj import ClientInfoObj
from random import randint

class AuthenticationHelper:
    def __init__(self, server_global):
        self.my_global = server_global

    def matchpasswd(self,login,passwd):
        """
        with open('info.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            handle.close()
            if reader.has_key(login) and reader[login] == passwd:
                return '#'
            else:
                token = randint(1,65565)
                self.my_global.active_user_directory[token] = self.my_ClientInfo
                return token.to_s()
        """
        #Using for testing since above won't work...
        try:
            if (self.my_global.test_login_database[login] == passwd):
                token = randint(1,65565)
                return token
            else:
                return -1
        except:
            return -1

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

