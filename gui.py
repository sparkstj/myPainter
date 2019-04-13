from tkinter import *
from tkinter import ttk
import algorithms

class App(object):
    def __init__(self, master):
        #self.default = Button(mainframe, text='greetings', command = algorithms.sayhello).grid(column=3, row=3, sticky=W)
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        intro = Label(self.mainframe, text="Drawing Functions:").grid(column=1, row=1, sticky=W)
        board = Tk()
        board.title('Drawing Board')
        self.canvas = Canvas(board)
        self.id = 0
        self.resetCanvas()
        self.saveCanvas()
        self.setColor()
        self.drawLine()
        self.drawPolygon()
        self.drawEllipse()
        self.drawCurve()
        self.translate()
        self.rotate()
        self.scale()
        self.clip()

    def resetCanvas(self):
        '''row = 2'''
        width_label = Label(self.mainframe, text="width:").grid(column=2, row=2, sticky=W)
        width = StringVar()
        width_entry = Entry(self.mainframe, textvariable=width).grid(column=3,row=2,sticky=W)
        height_label = Label(self.mainframe, text="height:").grid(column=4, row=2, sticky=W)
        height = StringVar()
        height_entry = Entry(self.mainframe, textvariable=height).grid(column=5,row=2,sticky=W)
        width_button = Button(self.mainframe, text='Reset Canvas', command = lambda: algorithms.resetCanvas(width,height,self.canvas)).grid(column=1,row=2,sticky=W)
    
    def saveCanvas(self):
        '''row = 3'''
        name_label = Label(self.mainframe, text="name:").grid(column=2, row=3, sticky=W)
        name = StringVar()
        name_entry = Entry(self.mainframe, textvariable=name).grid(column=3,row=3,sticky=W)
        name_button = Button(self.mainframe, text="Save Canvas", command = lambda: algorithms.saveCanvas(name, self.canvas)).grid(column=1,row=3,sticky=W)
    
    def setColor(self):
        '''row = 4'''
        r = StringVar()
        g = StringVar()
        b = StringVar()
        r_label = Label(self.mainframe, text="R:", justify=CENTER).grid(column=2,row=4,sticky=W)
        r_entry = Entry(self.mainframe, textvariable=r).grid(column=3,row=4,sticky=W)
        g_label = Label(self.mainframe, text="G:", justify=CENTER).grid(column=4,row=4,sticky=W)
        g_entry = Entry(self.mainframe, textvariable=g).grid(column=5,row=4,sticky=W)
        b_label = Label(self.mainframe, text="B:").grid(column=6,row=4,sticky=W)
        b_entry = Entry(self.mainframe, textvariable=b).grid(column=7,row=4,sticky=W)
        rgb_button = Button(self.mainframe, text="Set Color", command= lambda: algorithms.setColor(r,g,b,self.canvas)).grid(column=1,row=4,sticky=W)
    
    def drawLine(self):
        '''row = 5'''
        self.id = self.id + 1
        endpoint1_label = Label(self.mainframe, text="Endpoint1:").grid(column=2,row=5,sticky=W)
        endpoint1 = StringVar()
        endpoint2 = StringVar()
        endpoint1_entry = Entry(self.mainframe, textvariable=endpoint1).grid(column=3,row=5,sticky=W)
        endpoint2_label = Label(self.mainframe, text="Endpoint2:").grid(column=4,row=5,sticky=W)
        endpoint2_entry = Entry(self.mainframe, textvariable=endpoint2).grid(column=5,row=5,sticky=W) 

        algorithm_label = Label(self.mainframe, text='Algorithm:').grid(column=6,row=5,sticky=W)
        algorithm = StringVar()
        options = ["DDA","bresenham"]
        algorithm.set(options[0])
        algorithm_om = OptionMenu(self.mainframe, algorithm, *options)
        algorithm_om.grid(column=7,row=5,sticky=W)
        endpoints_button = Button(self.mainframe, text="Draw Line", command= lambda: algorithms.drawLine(self.id, endpoint1, endpoint2, algorithm, self.canvas)).grid(column=1,row=5,sticky=W)
    
    def drawPolygon(self):
        '''row = 6'''
        self.id = self.id + 1
        vertices_label = Label(self.mainframe, text='Vertices:').grid(column=2,row=6,sticky=W)
        vertices = StringVar()
        vertices_entry = Entry(self.mainframe, textvariable=vertices).grid(column=3,row=6,sticky=W)
        n_label = Label(self.mainframe, text='number:').grid(column=4,row=6,sticky=W)
        n = StringVar()
        n_entry = Entry(self.mainframe, textvariable=n).grid(column=5,row=6,sticky=W)
        
        algorithm_label = Label(self.mainframe, text='Algorithm:').grid(column=6,row=6,sticky=W)
        algorithm = StringVar()
        options = ["DDA","bresenham"]
        algorithm.set(options[0])
        algorithm_om = OptionMenu(self.mainframe, algorithm, *options)
        algorithm_om.grid(column=7,row=6,sticky=W)
        draw_button = Button(self.mainframe, text="Draw Polygon", command= lambda: algorithms.drawPolygon(self.id, vertices, n, algorithm, self.canvas)).grid(column=1,row=6,sticky=W)
    
    def drawEllipse(self):
        '''row=7'''
        self.id = self.id + 1
        center_label = Label(self.mainframe, text="Center:").grid(column=2,row=7,sticky=W)
        center = StringVar()
        center_entry = Entry(self.mainframe, textvariable=center).grid(column=3,row=7,sticky=W)
        r_label = Label(self.mainframe, text='Radius:').grid(column=4,row=7,sticky=W)
        r = StringVar()
        r_entry = Entry(self.mainframe, textvariable=r).grid(column=5,row=7,sticky=W)
        algorithm_label = Label(self.mainframe, text='Algorithm:').grid(column=6,row=7,sticky=W)
        algorithm = StringVar()
        options = ["DDA","bresenham"]
        algorithm.set(options[0])
        algorithm_om = OptionMenu(self.mainframe, algorithm, *options)
        algorithm_om.grid(column=7,row=7,sticky=W)
        draw_button = Button(self.mainframe, text="Draw Ellipse", command= lambda: algorithms.drawPolygon(self.id, center, r, algorithm, self.canvas)).grid(column=1,row=7,sticky=W)
    
    def drawCurve(self):
        '''row = 8'''
        self.id = self.id + 1
        points_label = Label(self.mainframe, text="Points:").grid(column=2,row=8,sticky=W)
        points = StringVar()
        points_entry = Entry(self.mainframe, textvariable=points).grid(column=3,row=8,sticky=W)
        n_label = Label(self.mainframe, text='number:').grid(column=4,row=8,sticky=W)
        n = StringVar()
        n_entry = Entry(self.mainframe, textvariable=n).grid(column=5,row=8,sticky=W)
        algorithm_label = Label(self.mainframe, text='Algorithm:').grid(column=6,row=8,sticky=W)
        algorithm = StringVar()
        options = ["DDA","bresenham"]
        algorithm.set(options[0])
        algorithm_om = OptionMenu(self.mainframe, algorithm, *options)
        algorithm_om.grid(column=7,row=8,sticky=W)
        draw_button = Button(self.mainframe, text="Draw Curve", command= lambda: algorithms.drawPolygon(self.id, points, n, algorithm, self.canvas)).grid(column=1,row=8,sticky=W)
    
    def translate(self):
        '''row = 9'''
        self.id = self.id + 1
        vector_label = Label(self.mainframe, text="Translation Vector:").grid(column=2,row=9,sticky=W)
        vector = StringVar()
        vector_entry = Entry(self.mainframe, textvariable=vector).grid(column=3,row=9,sticky=W)
        translate_button = Button(self.mainframe, text="Translate", command= lambda: algorithms.translate(self.id, vector, self.canvas)).grid(column=1,row=9,sticky=W)
    
    def rotate(self):
        '''row = 10'''
        self.id = self.id + 1
        center_label = Label(self.mainframe, text="Center:").grid(column=2,row=10,sticky=W)
        center = StringVar()
        center_entry = Entry(self.mainframe, textvariable=center).grid(column=3,row=10,sticky=W)
        r_label = Label(self.mainframe, text='Rotation Angle:').grid(column=4,row=10,sticky=W)
        r = StringVar()
        r_entry = Entry(self.mainframe, textvariable=r).grid(column=5,row=10,sticky=W)
        rotate_button = Button(self.mainframe, text="Rotate", command= lambda: algorithms.rotate(self.id, center, r, self.canvas)).grid(column=1,row=10,sticky=W)

    def scale(self):
        '''row = 11'''
        center_label = Label(self.mainframe, text="Center:").grid(column=2,row=11,sticky=W)
        center = StringVar()
        center_entry = Entry(self.mainframe, textvariable=center).grid(column=3,row=11,sticky=W)
        s_label = Label(self.mainframe, text='Scaling Parameter:').grid(column=4,row=11,sticky=W)
        s = StringVar()
        s_entry = Entry(self.mainframe, textvariable=s).grid(column=5,row=11,sticky=W)
        scale_button = Button(self.mainframe, text="Scale", command= lambda: algorithms.scale(self.id, center, r, self.canvas)).grid(column=1,row=11,sticky=W)

    def clip(self): 
        '''row = 12'''
        upperleft_label = Label(self.mainframe, text="UpperLeft Point:").grid(column=2,row=12,sticky=W)
        upperleft = StringVar()
        upperleft_entry = Entry(self.mainframe, textvariable=upperleft).grid(column=3,row=12,sticky=W)
        downright_label = Label(self.mainframe, text="DownRight Point:").grid(column=4,row=12,sticky=W)
        downright = StringVar()
        downright_entry = Entry(self.mainframe, textvariable=downright).grid(column=5,row=12,sticky=W)
        algorithm_label = Label(self.mainframe, text='Algorithm:').grid(column=6,row=12,sticky=W)
        algorithm = StringVar()
        options = ["Cohen-Sutherland","Liang-Barsky"]
        algorithm.set(options[0])
        algorithm_om = OptionMenu(self.mainframe, algorithm, *options)
        algorithm_om.grid(column=7,row=12,sticky=W)
        clip_button = Button(self.mainframe, text="Clip").grid(column=1, row=12, sticky=W)
        

root = Tk()
root.title('Graphics Menu')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

app = App(root)
#for child in root.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

mainloop()