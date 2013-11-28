__author__ = 'Kevin'

import pickle
import ServerGlobal
import string
import sys
import os

source_users = 'user_database.pkl'
source_connections = 'user_connection_log.pkl'



def load_users():
    global user_database
    try:
        with open('user_database.pkl'):
            print "Reading from database"
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
            print "Reading from database"
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
    print "shell commands enabled, type \"exit\" to return to the console"
    while True:
        inputc = raw_input("Shell command:")
        
        if inputc == "exit":
            return
        os.system(inputc)

def remove_user_from_db(user):
    load_users()
    if user_database[user] != None:
        del user_database[user]
        save_users()
        print "User \'{}\' removed".format(user)
        return True
    return False
    
#K    
def change_user_password(user,npword):
    load_users()
    if user_database[user] != None:
        user_database[user][0] = npword
        save_users()
        print "{}'s password changed!".format(user)
        return True
    return False

def view_user_files(user,path,remove):
    load_users()
    if user_database[user] != None:
        print "Found user {}".format(user)
        id = user_database[user][1]
        view_files(path+str(id)+'\\one_dir\\')
        if remove == True:
            delete_user_files(path+str(id)+'\\one_dir\\')
    else:
        print "user not found"
			
def delete_user_files(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            print "deleting file at {}".format(os.path.join(root,name))
            os.remove(os.path.join(root, name))
        for name in dirs:
            print "deleting directory {}".format(os.path.join(root, name))
            os.rmdir(os.path.join(root, name))
	
def view_files(path):
    count = 0
    size = 0
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
            count = count+1
            size = size + os.path.getsize(path)
    
    print "Directory has {} files and contains {} bytes".format(count,size)

def view_users():
    load_users()
    print string.rjust("username",1), string.rjust("password",2), string.rjust("id",3),string.rjust("online status",4)
    for i in user_database:
        if user_database[i][2] == 1:
            on = "ONLINE"
        else:
            on = "OFFLINE"
        print string.rjust(i,1), string.rjust(str(user_database[i][0]),2), string.rjust(str(user_database[i][1]),3),string.rjust(on,4)
	
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
            print "removefiles [username] - remove all of user\'s files"
            print "exit - exits console"
        
        elif parse[0] == "view":
            if parse[1] == "users":
                view_users()
            elif parse[1] == "connections":
                load_connection_history()
                print connection_database
            elif parse[1] == "files":
                view_files(server_info.server_global_directory)
            else:
                print "invalid command"
                
        elif parse[0] == "shellmode":
            shell_mode()
    
        elif parse[0] == "removeuser":
            if parse[2] == "-f":
                view_user_files(parse[1],server_info.server_global_directory,True)
				
            remove_user_from_db(parse[1])
        
        elif parse[0] == "changepword":
            change_user_password(parse[1],parse[2])
        
        elif parse[0] == "removefiles":
            view_user_files(parse[1],server_info.server_global_directory,True)

        elif parse[0] == "exit":
            print "exiting console"
            sys.exit()
			
        else:
            print "invalid command"

    load_users()
    load_connection_history()
    print user_database
    print connection_database

if __name__ == "__main__":
    main()
