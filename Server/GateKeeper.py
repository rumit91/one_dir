__author__ = 'AlexQu'
#!/usr/bin/python

import sys
import pickle
import ClientInfoObj
from random import randint

class ActiveUser:
    ActiveUserDirectory = {}

class Authentication:
    def matchpasswd(self,login,passwd):
        saveActiveUser = ActiveUser()
        self.my_ClientInfo = ClientInfoObj
        with open('info.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            handle.close()
            if reader.has_key(login) and reader[login] == passwd:
                return '#'
            else:
                token = randint(1,65565)
                saveActiveUser.ActiveUserDirectory[token] = self.my_ClientInfo
                return token.to_s()

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

#my_run = Authentication()
#print my_run.run("alex Qu1")
#print my_run.run("alex Qu")
