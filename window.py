from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
from tkinter_common import *
from data_form import *

import socket
from utils import *
import rsa
import pickle
import serpent

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        default_init(self, parent)
        self.resizable(True, True)
        self.edit_field = ScrolledText(self, highlightthickness=0)
        self.edit_field.pack(expand=True, fill='both')
        self.init_menu()
        center_window(self)

        self.create_rsa_key()
        self.get_session_key()            


    def create_rsa_key(self):
        self.public_rsa, self.private_rsa = rsa.generate(1024)
        with open('id_rsa', 'wb') as f:
            f.write(pickle.dumps(self.public_rsa))
        with open('id_rsa.pub', 'wb') as f:
            f.write(pickle.dumps(self.private_rsa))


    def get_session_key(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            send_request(sock, 'rsa_public', self.public_rsa)

            print('getting session_key')
            response = read_object(sock)
            self.session_key = rsa.decrypt(self.private_rsa, response['data'])
            self.session_id = response['session_id']
            print('done')


    def init_menu(self):
        menubar = Menu(self)
 
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Save as...', command=self.save_file_as)
        filemenu.add_command(label='Exit', command=self.terminate)

        menubar.add_cascade(label='File', menu=filemenu) 
        self.config(menu=menubar)

 
    def get_file_from_server(self, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print('sending filename {}'.format(filename))
            send_request(sock, 'get_file', filename, self.session_id)
            print('done')
            print('getting text')
            response = read_object(sock)
            print('done')
            assert(response['type'] == 'file')
            encrypted_text = response['data']

        return serpent.decrypt(self.session_key, encrypted_text)


    def open_file(self):
        data = (('Path', 'str'),)
        @messageboxed
        def callback(data):
            resp = self.get_file_from_server(data['Path'])
            if resp == '':
              raise('There is no such file')
            self.edit_field.delete(1.0, END)
            self.edit_field.insert(END, resp)
 
        DataWindow(self, data, 'Open', callback)
 

    def send_file_to_server(self, path):
        text = self.edit_field.get(1.0, END)
        if text[-1] == '\n':
            text = text[:-1]
        text = serpent.encrypt(self.session_key, text)

        req = {'filename': path, 'text': text}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print('sending text')
            send_request(sock, 'save_file', req, self.session_id)
            print('done')


    def save_file_as(self):
        data = (('Path', 'str'),)
 
        @messageboxed
        def callback(data):
            self.send_file_to_server(data['Path'])
 
        DataWindow(self, data, 'Save', callback) 
 

def messageboxed(func):
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
            showinfo('Info', 'Success')
            return True
        except Exception as e:
            showerror('Error', str(e))
            return False
 
    return wrapped


if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()
    Window(root)
    root.mainloop()