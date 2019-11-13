HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

import pickle 

def send_object(socket, obj):
	socket.sendall(pickle.dumps(obj))

def read_string(socket):
	text = b''
	while True:
		data = socket.recv(1024)
		if not data:
			break
		text = text + data
		if len(data) < 1024:
			break
	return pickle.loads(text)