__author__ = 'AlexQu'
#!/usr/bin/python

import sys
import pickle

"""USAGE:The function returns True if the user and passwd match False otherwise"""
class ActiveUserDirectory:
    """is it a class or a single file like .pickle"""

class GateKeeper:
    def matchpasswd(login,passwd):
        with open('userinfo.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            if reader.has_key(login) and reader[login] == passwd:
                return True
            else:
                return False

    def createUser(login,passwd):
        # read in csv file to check for unique user_id, return False if user_id exists
        tmp = False
        with open('userinfo.pickle', 'rb') as handle:
            reader = pickle.load(handle)
            if reader.has_key(login):
                return False
            else:
                tmp = True
        if tmp == True:
            with open('userinfo.pickle','wb') as handle:
                reader[login] = passwd
                pickle.dump(reader,handle)
                ## return True if user created
                return True

    while True:
        command = sys.stdin.readline()
        command = command.strip()
        print "Type in 'Username Password'"
        # read a line from stdin
        line = sys.stdin.readline()
        # remove '\n' from line
        line = line.strip()
        # extract username and password from line
        username = line[:line.find(' ')]
        password = line[line.find(' ')+1:]
        if matchpasswd(username, password):
            print 'Successfully Logged in\n'
            """create token """

            """store token + client InfoObj"""

        else:
            print 'Login Failed\n'
            break



    """
    elif command == 'create':
        print "Type in 'Username Password'"
        line = sys.stdin.readline()
        line = line.strip()
        usernameCreate = line[:line.find(' ')]
        passwordCreate = line[line.find(' ')+1:]
        if createUser(usernameCreate, passwordCreate):
            print 'User Created.\n'
        else:
            print 'ERR. User exists\n'
    elif command == 'exit':
        break
    """