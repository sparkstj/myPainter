from tkinter import *
from tkinter import ttk
import algorithms

   

root = Tk()
root.title('Graphics Menu')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

width_label = Label(mainframe, text="width:").grid(column=2, row=1, sticky=W)
width = StringVar()
width_entry = ttk.Entry(mainframe, textvariable=width).grid(column=3,row=1,sticky=W)
height_label = Label(mainframe, text="height:").grid(column=4, row=1, sticky=W)
height = StringVar()
height_entry = Entry(mainframe, textvariable=height).grid(column=5,row=1,sticky=W)
width = width.get()
height = height.get()
print(width, height)
width_button = Button(mainframe, text='Reset Canvas', command = lambda: algorithms.resetCanvas(width,height)).grid(column=1,row=1,sticky=W)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()