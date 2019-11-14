import socket
from utils import *

import numpy as np
import rsa
import serpent
import os

clients_rsa_keys = {}
clients_session_keys = {}

def get_new_session_id():
    global_session_id = 0
    fail = True
    while fail:
        try:
            os.mkdir(str(global_session_id))
            fail = False
        except:
            global_session_id += 1
    return global_session_id
                        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            while True:
                request = read_object(conn)
                print('Got request:')
                print(request)
                if request is None:
                    break

                if request['type'] == 'rsa_public':
                    session_id = get_new_session_id()
                    clients_rsa_keys[session_id] = request['data']
                    session_key = serpent.create_key(16)
                    clients_session_keys[session_id] = session_key
                    
                    print('Sending session_key')
                    encrypted_session_key = rsa.encrypt(clients_rsa_keys[session_id], session_key)
                    send_request(conn, 'session_key', encrypted_session_key, session_id)
                    print('done')

                if request['type'] == 'get_file':
                    filename = request['data']
                    session_id = request['session_id']
                    print('Query: {}'.format(filename))
                    try:
                        with open('texts/{}'.format(filename), 'r') as file:
                            text = ' '.join(file.readlines())[:1000]
                    except:
                        text = ''

                    session_key = clients_session_keys[session_id]
                    encrypted_text = serpent.encrypt(session_key, text)
                    print('Sending text file')
                    send_request(conn, 'file', encrypted_text)
                    print('done')

                if request['type'] == 'save_file':
                    data = request['data']
                    filename = data['filename']
                    enc_text = data['text']
                    session_key = clients_session_keys[request['session_id']]
                    text = serpent.decrypt(session_key, enc_text)
                    with open('{}/{}'.format(session_id, filename), 'w') as f:
                        f.write(text)

