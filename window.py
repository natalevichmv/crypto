import tkinter as tk

import socket
from utils import *
import rsa
import pickle
import serpent

def create_texter():
  master = tk.Tk()

  tk.Label(master, 
           text="Desired filename").grid(row=0)

  filename_field = tk.Entry(master)
  filename_field.grid(row=0, column=1)

  tk.Button(master, 
            text='Quit', 
            command=master.quit).grid(row=3, 
                                      column=0, 
                                      sticky=tk.W, 
                                      pady=4)
  tk.Button(master, 
            text='Enter', command=get_file_func).grid(row=3, 
                                                      column=1, 
                                                      sticky=tk.W, 
                                                      pady=4)

def get_rsa_length():  
    try:
      public, private = rsa.generate(rsa_len_field.get())
    except:
      return None
    with open('id_rsa', 'wb') as f:
        f.write(pickle.dumps(public))
    with open('id_rsa.pub', 'wb') as f:
        f.write(pickle.dumps(private))

    create_texter()

def create_start_screen():
  master = tk.Tk()

  tk.Label(master, 
           text="RSA key length").grid(row=0)

  rsa_len_field = tk.Entry(master)
  rsa_len_field.grid(row=0, column=1)

  tk.Button(master, 
            text='Quit', 
            command=master.quit).grid(row=3, 
                                      column=0, 
                                      sticky=tk.W, 
                                      pady=4)
  tk.Button(master, 
            text='Enter', command=get_rsa_length).grid(row=3, 
                                                          column=1, 
                                                          sticky=tk.W, 
                                                          pady=4)
  tk.mainloop()


if __name__ == '__main__':
  create_start_screen()