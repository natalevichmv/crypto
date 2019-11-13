import socket
from utils import *

import numpy as np
import rsa
import serpent

clients_rsa_keys = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        rsa_public = read_string(conn)
        clients_rsa_keys[addr] = rsa_public
        session_key = serpent.create_key(16)
        send_object(conn, rsa.encrypt(clients_rsa_keys[addr], session_key))

        while True:
            try:
                filename = read_string(conn)
            except EOFError:
                break
            print('Query: {}'.format(filename))

            with open('texts/{}'.format(filename), 'r') as file:
                text = ' '.join(file.readlines())[:1000]
            encrypted_text = serpent.encrypt(session_key, text)
            send_object(conn, encrypted_text)

