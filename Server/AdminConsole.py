__author__ = 'Kevin'

import pickle
import ServerGlobal


source_users = 'user_database.pkl'
source_connections = 'user_connections_database.pkl'
global user_database = {}
global connection_database = {}

def load_users(self):
    try:
        with open('user_database.pkl'):
            print "Found saved user database"
            user_database = pickle.load(open(source_users, 'rb'))
            except IOError:
        print "No previous user database was found"
	
def save_users(self):
    output = open('user_database.pkl','wb')
	pickle.dump(user_database,output)
	output.close()
	
def save_connection_history(self):
	output = open('user_database_connections.pkl','wb')
	pickle.dump(connection_database,output)
	output.close()

def load_connection_history(self):
    try:
        with open('user_database.pkl'):
            print "Found saved user database"
            connnection_database = pickle.load(open(source_connections,'rb'))
    except IOError:
        print "No previous user database was found"

def print_users(self):
    for k,v in user_database:
        print k
	
def print_connections(self):
    for k,v in connection_database:
        print k
        for i,j in v:
            print j[0],j[1] #print connection history in list

def shell_mode(self):
    while true:
        inputc = input("Shell command:")
        if inputc == "exit":
            return
        os.system(inputc)
		
def key_file_to_path(self):
    #tbd
	
def remove_user_from_db(self, user):
    self.load_users()
    if user_database[user] != nil:
        del user_database[user]
        return True
    return False
	
def change_user_password(self,user,npword):
    self.load_users()
    if user_database[user] != nil:
        user_database[user][0] = npword
		self.save_users()
        return True
    return False