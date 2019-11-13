import socket
from utils import *
import rsa
import pickle
import serpent

public, private = rsa.generate(1024)
with open('id_rsa', 'wb') as f:
    f.write(pickle.dumps(public))
with open('id_rsa.pub', 'wb') as f:
    f.write(pickle.dumps(private))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    send_object(sock, public)
    session_key = rsa.decrypt(private, read_string(sock))

    while True:
    	print('Print the name of the desired file:')
    	filename = input()
    	if not len(filename):
    		break
    	send_object(sock, filename)
    	encrypted_text = read_string(sock)
    	text = serpent.decrypt(session_key, encrypted_text)
    	print(text)
    	print()