__author__ = 'Kevin'

import pickle
import ServerGlobal
import os

source_users = 'user_database.pkl'
source_connections = 'user_connection_log.pkl'



def load_users():
    global user_database
    try:
        with open('user_database.pkl'):
            print "Found saved user database"
            user_database = pickle.load(open(source_users, 'rb'))
    except IOError:
        print "No previous user database was found"
    
def save_users():
    output = open('user_database.pkl','wb')
    pickle.dump(user_database,output)
    output.close()

def load_connection_history():
    global connection_database
    try:
        with open('user_connection_log.pkl'):
            print "Found saved user database"
            connection_database = pickle.load(open(source_connections,'rb'))
    except IOError:
        print "No previous user database was found"
        
#H(1/2)
def print_users():
    for k,v in user_database:
        print k
#L(1/2)    
def print_connections():
    for k,v in connection_database:
        print k
        for i,j in v:
            print j[0],j[1] #print connection history in list

            
def shell_mode():
    while true:
        inputc = input("Shell command:")
        if inputc == "exit":
            return
        os.system(inputc)
    
#I    
#def key_file_to_path(self):
    #tbd
    
#J(1/2)
def remove_user_from_db(user):
    load_users()
    if user_database[user] != None:
        del user_database[user]
        save_users()
        return True
    return False
    
#K    
def change_user_password(user,npword):
    load_users()
    if user_database[user] != None:
        user_database[user][0] = npword
        save_users()
        return True
    return False
    
def view_user_files(user_path):
    for root, dirs, files in os.walk(user_path):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
            
def main():
    server_info = ServerGlobal.ServerGlobal()
    print "OneDir Console v.9 \"help\" for usage information."
    
    
    while True:
        inputc = raw_input('Enter Command:')
        parse = inputc.split(" ")
    
        if parse[0] == "help":
            print "view [users] or [connections] [files <username>] - displays information on target"
            print "changepword [username] [newpassword] - changes user password if username found"
            print "shellmode - pipelines commands to OS terminal"
            print "removeuser [username] [-f] - removes user profile, -f includes file removal"
        
        elif parse[0] == "view":
            if parse[1] == "users":
                load_users()
                print user_database
            elif parse[1] == "connections":
                load_connection_history()
                print connection_database
        elif parse[1] == "files":
                view_user_files(server_info.server_global_directory)
                
        elif parse[0] == "shellmode":
            shell_mode()
    
        elif parse[0] == "removeuser":
            remove_user_from_db(parse[1])
        
        elif parse[0] == "changepword":
            change_user_password(parse[1],parse[2])
            
        else:
            print "invalid command"

    load_users()
    load_connection_history()
    print user_database
    print connection_database

    
if __name__ == "__main__":
    main()
