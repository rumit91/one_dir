#!/usr/bin/env python
import socket
from threading import Thread


#super class
class Communicator:
	 def __init__(self, my_host_name='', my_port=-1, target_host_name='', target_port=-1, global_info=None):
		self.my_host_name = my_host_name
		self.my_port = my_port
		self.target_host_name = target_host_name
		self.target_port = target_port
		self.global_info = global_info


class Messenger(Communicator):
	 def _connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.target_host_name, self.target_port))

	 #returns true if message is sent completely
	 def send(self, message):
		try:
		  self._connect()
		  status = self.sock.sendall(message)
		  self.sock.close()
		except socket.error:
		  #in case of failure, intiate a resend protocol
		  return False

		return True


class Receiver(Communicator):
	 def setup(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.my_host_name, self.my_port))

	 def client_handle(self, connection,addr):
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

	 def dispatch(self, message):
		print message

	 #begins listening
	 def spin(self):
		#up to 8 concurrent connections
		self.sock.listen(8)
		while 1:
		  #fire off a thread to accept and handle incoming messages
		  conn, addr = self.sock.accept()
		  ClientHandleThread = Thread(target=self.client_handle(conn,addr))
		self.sock.close()

class AuthReceiver(Receiver):
	def client_handle(self,connection,addr):
		message_raw = []
		while True:
			data = connection.recv(4096)
			if not data:
				break
			#append message to list
			message_raw.append(data)

		#concatenate to single string
		message = ''.join(message_raw)

		saveActiveUser = ActiveUser()
		self.my_ClientInfo = ClientInfoObj
		self.token = -1
		
		parsed = message.split('|')
		if message[0] == '0':
			self.dispatch(GateKeeper.Authentication.createUser(message[1],message[2]),addr)
		else:
			self.dispatch(GateKeeper.Autentication.matchpasswd(message[1],message[2]),addr)
		
		def dispatch(self, message,addr):
			nsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			auth_messenger = nsock.connect(addr,12349)
			try:
				status = nsock.sendall(message)
			except socket.error:
		  #in case of failure, intiate a resend protocol
				dispatch(message,addr)
				

class CommUnit:
	 def __init__(self, host_name, event_port=-1, file_request_port=-1, file_port=-1, gatekeeper_port=-1):
		self.host_name = host_name
		self.event_port = event_port
		self.file_request_port = file_request_port
		self.file_port = file_port
		self.gatekeeper_port = gatekeeper_port

