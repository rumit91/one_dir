#!/usr/bin/env python
import socket
import sys
from threading import Thread

#super class
class Communicator:
	def __init__(self,host_name,port):
		self.port = port
		self.host_name = host_name


class Messenger(Communicator):

	def _connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(self.host_name,self.port)

	#returns true if message is sent completely
	def send(self,message):
		try:
			self._connect()
			status = self.sock.sendall(message)
			self.sock.close()
		except socket.error:
			#in case of failure, intiate a resend protocol
			return False

		return True

class Reciever(Communicator):

	def setup(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(self.host_name,self.port)

	def client_handle(self, connection):
		#message list
		message_raw = []
		while True:
			data = connection.recv(4096)
			if not data:
				break
			#append message to list
			message_raw.append(data)

		#concatenate to single string
		message = ''.join(message_raw)

		#add check for delimiter here (TBD)

		#parse in dispatch function
		self.dispatch(message)

	#begins listening
	def spin(self):
		#up to 8 concurrent connections
		self.sock.listen(8)
		while 1:
			#fire off a thread to accept and handle incoming messages
			conn, addr = self.sock.accept()
			ClientHandleThread = Thread(target = self.client_handle(conn))
		self.sock.close()
