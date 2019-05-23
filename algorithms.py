from tkinter import *
from tkinter import ttk

__author__ = 'Jing Tan'

brushColor = "#476042"

def drawPixel(x, y, canvas):
    canvas.create_rectangle(x, y, x, y, fill=brushColor)

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
        if (algorithm=="DDA"):
            (xstart, ystart) = p1
            (xend, yend) = p2
            dx = xend - xstart
            dy = yend - ystart
            x, y = xstart, ystart

            steps = max(abs(dx), abs(dy))
            drawPixel(int(x), int(y), canvas)
        
            xInc = dx / steps
            yInc = dy / steps

            for i in range(steps):  
                x = x + xInc
                y = y + yInc
                drawPixel(int(x), int(y), canvas)
        print(id, p1, p2, algorithm)

        if (algorithm=="Bresenham"):
            (xstart, ystart) = p1
            (xend, yend) = p2
            dx = xend - xstart
            dy = yend - ystart
            m = dy / dx
            dx = abs(dx)
            dy = abs(dy)
            dx_2 = 2 * dx
            dy_2 = 2 * dy
            dxsdy_2 = 2 * (dx - dy)
            dysdx_2 = 2 * (dy - dx)
            #print(m)
            if (m > 1):
                p = 2 * dx - dy
                if (ystart > yend):
                    x = xend
                    y = yend
                    yend = ystart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas)
                while (y < yend):
                    y = y + 1
                    if p < 0:
                        p = p + dx_2
                    else:
                        x = x + 1
                        p = p + dxsdy_2
                    drawPixel(x, y)
            elif m == 1:
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas)
                while (x < xend):
                    x = x + 1
                    y = y + 1
                    drawPixel(x, y, canvas)
            elif (m>0) and (m<1):
                p = 2 * dy - dx
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas)
                while (x < xend):
                    x = x + 1
                    if p < 0:
                        p = p + dy_2
                    else:
                        y = y + 1
                        p = p + dysdx_2
                    drawPixel(x, y, canvas)
            elif (m > -1) and (m < 0):
                p = 2 * dy - dx
                if xstart < xend:
                    x = xend
                    y = yend
                    xend = xstart
                else: 
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas)
                while (x > xend):
                    x = x - 1
                    if p < 0:
                        p = p + dy_2
                    else:
                        y = y + 1
                        p = p + dysdx_2
                    drawPixel(x,y,canvas)
            elif m == -1.0:
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas)
                while (x < xend):
                    x = x + 1
                    y = y - 1
                    drawPixel(x,y,canvas)
            elif m < -1:
                p = 2*dx-dy
                if ystart < yend:
                    x = xend
                    y = yend
                    yend = ystart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas)
                while (y > yend):
                    y = y - 1
                    if p < 0:
                        p = p + dx_2
                    else:
                        x = x + 1
                        p = p + dxsdy_2
                    drawPixel(x,y,canvas)
            else:
                #print("hi")
                if (xstart == xend):
                    y = min(ystart, yend)
                    x = xstart
                    for i in range(dy):
                        drawPixel(x,y,canvas)
                        y = y + 1
                elif ystart == yend:
                    x = min(xstart, xend)
                    y = ystart
                    for i in range(dx):
                        drawPixel(x,y,canvas)
                        x = x + 1
         
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
