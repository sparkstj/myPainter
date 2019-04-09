from tkinter import *

class App(object):
    def __init__(self, master):
        self.com = Button(master, text='greetings', command = self.say_hello)
        self.com.pack(side = "top")
    
    def say_hello(self):
        print('hello, tkinter GUI!')

root = Tk()
root.title('window with command')
root.geometry('400x200')

app = App(root)
root.mainloop()