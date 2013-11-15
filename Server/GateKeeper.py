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
        with open('info.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            handle.close()
            if reader.has_key(login) and reader[login] == passwd:
                return True
            else:
                return False

    def createUser(self,login,passwd):
        # read in csv file to check for unique user_id, return False if user_id exists
        tmp = False
        with open('info.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            handle.close()
            if reader.has_key(login):
                return False
            else:
                tmp = True
        if tmp == True:
            with open('info.pickle','wb') as handle:
                handle.close()
                reader[login] = passwd
                pickle.dump(reader,handle)
                ## return True if user created
                return True

    def run(self,info):
        saveActiveUser = ActiveUser()
        self.my_ClientInfo = ClientInfoObj
        self.token = -1
        line = info.strip()
        # extract username and password from line
        username = line[:line.find(' ')]
        password = line[line.find(' ')+1:]
        if self.matchpasswd(username, password):
            #print 'Successfully Logged in'
            self.token = randint(1,65565)
            """Dont know whether below really saves ClientInfoObj"""
            saveActiveUser.ActiveUserDirectory[self.token] = self.my_ClientInfo
            #print saveActiveUser.ActiveUserDirectory
            return self.token
        else:
            #print 'Login Failed\n'
            return self.token
        """If password and userid match record, it will return the token value(a random int from 1 to 65565).
        Else return token value of -1"""

#my_run = Authentication()
#print my_run.run("alex Qu1")
#print my_run.run("alex Qu")
