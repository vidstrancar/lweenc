import json
import socket
import struct

def build_dictionary(type, l):
    if type == 'register':
        content = {"type":type, "name":l[0], "n":l[1], "q":l[2], "m":l[3], "alpha":l[4], "A":l[5]}
    elif type == 'get_request':
        content = {"type":type, "name":l[0]}
    elif type == 'get_response': 
        content = {"type":type, "name":l[0], "n":l[1], "q":l[2], "m":l[3], "alpha":l[4], "A":l[5]}
    elif type == 'private':
        content = {"type":type, "enc_msg": l}
    elif type == 'public':
        content = {"type":type, "msg":l[0]}
    else:
        raise Exception("Exception in message_to_dict.")
    return content

def send_dictionary(sock, dictionary):
    msg = json.dumps(dictionary)
    msg = bytes(msg, "utf-8")
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    msg = recvall(sock, msglen)
    msg.decode("utf-8")
    return msg

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def recv_dictionary(sock):
    msg = recv_msg(sock)
    dictionary = json.loads(msg)
    return dictionary