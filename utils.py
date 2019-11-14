HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433        # The port used by the server

import pickle 

def send_object(socket, obj):
	socket.sendall(pickle.dumps(obj))

def send_request(socket, req_type, data, session_id=None):
	request = {'type': req_type, 
	           'session_id': session_id,
	           'data': data}
	send_object(socket, request)

def read_object(socket):
	text = b''
	while True:
		data = socket.recv(1024)
		if not data:
			break
		text = text + data
		if len(data) < 1024:
			break

	try:
		result = pickle.loads(text)
	except:
		result = None
	return result
	