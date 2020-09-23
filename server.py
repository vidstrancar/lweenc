import socket
import os
from _thread import start_new_thread

from communication import send_dictionary, recv_dictionary, build_dictionary
import csv_helper

server = socket.socket()
host = '127.0.0.1'
port = 1268

class Client:
	def __init__(self, socket, addr, port, clients):
		self.socket = socket
		self.addr = address
		self.port = port
		self.clients = clients		
	def send(self, msg):
		m = str.encode(msg)
		try:
			self.socket.sendall(m)
		except:
			clients.remove(client)
			self.socket.close()
	def broadcast(self, msg):
			m = str.encode(msg)
			for client in self.clients:
				if client != self:
					try:
						client.socket.sendall(m)
					except:
						clients.remove(client)
						client.socket.close()
						break
	def remove(self):
		self.socket.close()
		self.clients.remove(self)

def threaded_client(client):
	while True:
		try:
			content = recv_dictionary(client.socket)
			print(content)
			if content["type"] == 'register':
				csv_helper.save_to_csv("public_keys.csv", [content["name"], content["n"], content["q"], content["m"], content["alpha"], content["A"]])
			elif content["type"] == 'get_request':
				row = csv_helper.find_user_data_in_csv("public_keys.csv", content["name"])
				if row != None:
					msg = build_dictionary('get_response', [row[0], row[1], row[2], row[3], row[4], row[5]])
				else:
					msg = build_dictionary('get_response', [None, None, None, None, None, None])
				send_dictionary(client.socket, msg)
			elif content["type"] == 'public' or content["type"] == 'private':
				for c in client.clients:
					send_dictionary(c.socket, content)
		except:
			client.remove()
			break


try:
	server.bind((host, port))
except socket.error as e:
	print(str(e))

server.listen(5)

clients = [] 
while True:
	socket, address = server.accept()
	client = Client(socket, address[0], address[1], clients)
	clients.append(client)
	start_new_thread(threaded_client, (client, ))
	print('Connected to: ' + address[0] + ':' + str(address[1]))

server.close()
