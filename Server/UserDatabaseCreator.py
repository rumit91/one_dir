__author__ = 'Timur'
import pickle
import sys
import os

user_database = {'david': ('pass', 1), 'david1': ('pass2', 2)}
output = open('user_database.pkl', 'wb')
pickle.dump(user_database, output)