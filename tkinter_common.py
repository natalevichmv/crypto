def add_default_protocols(child, parent):
    def terminate():
        child.destroy()
        try:
            parent.terminate()
        except:
            parent.destroy()
    child.terminate = terminate
    child.protocol('WM_DELETE_WINDOW', child.terminate)
 
 
def default_init(child, parent):
    child.title('Crypto safe communication')
    child.parent = parent
    child.resizable(False, False)
    add_default_protocols(child, parent)
 
 
def center_window(window):
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    position_right = int(window.winfo_screenwidth()/2 - 100 - window_width/2)
    position_down = int(window.winfo_screenheight()/2 - 100 - window_height/2)
    window.geometry("+{}+{}".format(position_right, position_down))
