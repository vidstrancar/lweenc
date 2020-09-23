import socket
from _thread import start_new_thread
import csv

import lweenc
from communication import send_dictionary, recv_dictionary, build_dictionary

import csv_helper

def threaded_read_from_server(server):
	while True:
		content = recv_dictionary(server)
		if content["type"] == 'private':
			row = csv_helper.read_first_row("privates.csv")
			ld = lweenc.Lwe_decryptor(int(row[1]), int(row[2]), int(row[3]), float(row[4]), eval(row[5]), eval(row[6]))
			msg = ld.decrypt(content["enc_msg"])
			print('\033[91m' + content["type"] + ': ' + msg + '\033[0m')
		elif content["type"] == 'get_response':
			if content["name"] != None:
				csv_helper.save_to_csv("public_keys.csv", [content["name"], content["n"], content["q"], content["m"], content["alpha"], content["A"]])
		else:
			print('\033[91m' + content["type"] + ': ' + content["msg"] + '\033[0m')
		

server = socket.socket()
host = '127.0.0.1'
port = 1268

try:
	server.connect((host, port))
except socket.error as e:
	print(str(e))

start_new_thread(threaded_read_from_server, (server, ))

while True:
	cmd = input()
	words = cmd.split(' ')
	msg = None

	if words[0] == 'register':
		n = 50 #!!!!!!!!
		ld = lweenc.Lwe_decryptor(n)
		csv_helper.save_to_csv("privates.csv", [words[1], ld.n, ld.q, ld.m, ld.alpha, ld.s, ld.A])
		msg = build_dictionary('register', [words[1], ld.n, ld.q, ld.m, ld.alpha, ld.A])
	elif words[0] == 'get':
		msg = build_dictionary('get_request', [' '.join(words[1:])])
	elif words[0] == 'private':
		receiver = words[1]
		msg = ' '.join(words[2:])
		row = csv_helper.find_user_data_in_csv("public_keys.csv", receiver)
		if row != None:
			le = lweenc.Lwe_encryptor(int(row[1]), int(row[2]), int(row[3]), eval(row[5])) #OPASNO, kar se te eval pretvorbe string lista v list tiče
			msg_enc = le.encrypt(msg)
			msg = build_dictionary('private', msg_enc)
		else:
			print("No public key for " + receiver + " public_keys.csv")
			continue
	else:
		msg = build_dictionary('public', [' '.join(words)])

	send_dictionary(server, msg)
	 
server.close()