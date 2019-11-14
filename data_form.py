import re
import tkinter
import tkinter.messagebox 
import tkinter_common

class DataForm:
    def __init__(self, parent, data, action_name, callback):
        widgets = {}
        start_row = 0
        for name, t in data:
            label = tkinter.Label(parent, text=name+':')
            label.grid(row=start_row, column=0, sticky=tkinter.W)
 
            widgets[name] = DataForm._create_widget(t, parent)
            widgets[name].grid(row=start_row, column=1, sticky=tkinter.E)
 
            start_row += 1
 
        def command():
            res = {}
            for name, t in data:
                try:
                    res[name] = DataForm._get_data(widgets[name], name, t)
                except Exception as e:
                    tkinter.messagebox.showerror('Error', str(e))
                    return
            if callback(res):
                parent.destroy()
 
        action_button = tkinter.Button(parent, text=action_name, command=command)
        action_button.grid(row=start_row, column=0, sticky='news')
 
        exit_button = tkinter.Button(parent, text='Exit', command=(parent.destroy))
        exit_button.grid(row=start_row, column=1, sticky='news')
 
    @staticmethod
    def _create_widget(t, *args, **kwargs):
        if t in ['str', 'astr', 'date', 'phone', 'rsalen']:
            return tkinter.Entry(*args, **kwargs)
        if t == 'hidden_str':
            return tkinter.Entry(show='*', *args, **kwargs)
        raise Exception('Not implemented type {} in form'.format(t))
 
    @staticmethod
    def _get_data(w, name, t):
        if t in ['str', 'hidden_str', 'astr', 'date', 'phone', 'rsalen']:
            res = w.get()
            if t != 'astr' and not res:
                raise Exception("Field '{}' not filled".format(name))
            if t == 'date' and not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', res):
                raise Exception("Field '{}' filled incorrectly: date should be in format DD.MM.YYYY".format(name))
            if t == 'phone' and not re.fullmatch(r'\+?[0-9\-()]+', res):
                raise Exception('Invalid phone format')
            if t == 'rsalen' and not isrsalen(res):
                raise Exception('Number of bits in RSA key must be a power of 256 and >= 1024')
            return res
        raise Exception('Not implemented type {} in form'.format(t))
 
 
class DataWindow(tkinter.Toplevel):
    def __init__(self, parent, data, action_name, callback):
        super().__init__(parent)
        tkinter_common.default_init(self, parent)
 
        DataForm(self, data, action_name, callback)
        tkinter_common.center_window(self)
 
 
def isrsalen(x):
    if not re.fullmatch('[1-9]\d*', x):
        return False
    x = int(x)
    return x >= 1024 and x % 256 == 0