__author__ = 'Timur'
import pickle
import sys
import os

user_database = {'david': ['pass', 1,0], 'david1': ['pass2', 2,0]}
output = open('user_database.pkl', 'wb')
pickle.dump(user_database, output)
output.close()
print repr(open("user_database.pkl").read())
print repr(open("user_connection_log.pkl").read())
