__author__ = 'Kevin'
import pickle
import sys
import os

ActiveUserLog = {'user' : (('address','timestamp'))}
output = open('user_connection_log.pkl', 'wb')
pickle.dump(ActiveUserLog, output)
output.close()

