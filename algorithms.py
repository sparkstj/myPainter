from tkinter import *
from tkinter import ttk

__author__ = 'Jing Tan'


def sayhello():
    ''' default action.
    '''
    print("hello.")

def resetCanvas(width, height, canvas):
    '''clean the current canvas, reset canvas width and height, 
    width, height: int, 100 <= width, height <= 1000
    '''
    try:
        width = int(width.get())
        height = int(height.get())
        print(width, height, type(width), type(height))
        canvas.bind("<Configure>")
        canvas.width = width
        canvas.height = height
        canvas.config(width = canvas.width, height=canvas.height)
        canvas.pack(fill=BOTH, expand=YES)
        
    except ValueError:
        pass

def saveCanvas(name, canvas):
    '''save current canvas as name.bmp, 
    name: string
    '''
    name = name.get()
    print(name,type(name))

def setColor(R, G, B, canvas):
    '''set brush color, 
    0 <= R, G, B <= 255
    '''
    try:
        r, g, b = int(r.get()), int(g.get()), int(b.get())
        print(R,type(R),G,type(G),B,type(B))
    except ValueError:
        pass

def drawLine(id, p1, p2, algorithm, canvas):
    ''' id: unique identity for each primitive
     p1, p2: float tuples, denote the startpoint and endpoint coordinates
     algorithm: string, denotes drawing algorithm, eg:DDA or bresenham
     '''
    try:

        print(id, p1, p2, algorithm)
    except ValueError:
        pass

def drawPolygon(id, n, vertices, algorithm, canvas):
    ''' id: unique identity for each primitive
    n: number of vertices
    vertices: list of float tuples, denotes the polygon vertices
    algorithm: string, denotes drawing algorithm
    '''
    try:
        
        print(id,n,vertices,algorithm)
    except ValueError:
        pass

def drawEllipse(id, center, r, canvas):
    ''' id: unique identity for each primitive
    center: float tuple, denotes the center's coordinate
    r: float tuple, (major semi-axis, minor semi-axis)
    '''
    try:
        
        print(id, center, r)
    except ValueError:
        pass

def drawCurve(id, n, points, algorithm, canvas):
    ''' id: unique identity for each primitive
    n: int, number of points observed on the curve
    points: list of float tuples, denotes n observed points coordinate
    algorithm: string, denotes drawing algorithm
    '''
    try:
        
        print(id,n,points,algorithm)
    except ValueError:
        pass

def translate(id, d, canvas):
    ''' id: unique identity for each primitive
    d: float tuple, denotes the translation vector
    '''
    try:
        
        print(id, d)
    except ValueError:
        pass

def rotate(id, center, r, canvas):
    ''' id: unique identity for each primitive
    center = (x, y): float tuple, denotes the rotation center coordinate
    r: float, the angle of clockwise rotation
    '''
    try:
       
        print(id, center, r)
    except ValueError:
        pass

def scale(id, center, s, canvas):
    ''' id: unique identity for each primitive
    center = (x,y): float tuple, denotes the coordinate of scaling center
    s: float, denotes scale of scaling
    '''
    try:
        
        print(id,center,s)
    except ValueError:
        pass

def clip(id, p1, p2, algorithm, canvas):
    ''' id: unique identity for each primitive
    p1, p2: float tuples, denote up-left and down-right coordinate of target window
    algorithm: string, denotes the clipping algorithm.
    '''
    try:
        
        print(id,p1,p2,algorithm)
    except ValueError:
        pass
