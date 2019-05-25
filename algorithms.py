from tkinter import *
from tkinter import ttk
from Objects import Objects
import numpy as np
from math import *
import scipy.interpolate as si

__author__ = 'Jing Tan'

brushColor = "#476042"


def drawPixel(x, y, canvas, id, brushColor):
    variable = canvas.create_rectangle(x, y, x, y, fill=brushColor)
    if id != -1:
        Objects.obList[id].append(variable)
    

def Manhattan(p0, p1):
	(x0, y0) = p0
	(x1, y1) = p1
	return abs(x1-x0)+abs(y1-y0)

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
        if (algorithm=="DDA"): #This Implementation Combines the situation of 
            (xstart, ystart) = p1
            (xend, yend) = p2
            dx = xend - xstart
            dy = yend - ystart
            x, y = xstart, ystart

            steps = max(abs(dx), abs(dy))
            drawPixel(int(x), int(y), canvas, id, brushColor)
        
            xInc = dx / steps
            yInc = dy / steps

            for i in range(steps):  
                x = x + xInc
                y = y + yInc
                drawPixel(int(x), int(y), canvas, id, brushColor)
        

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
                drawPixel(x, y, canvas, id, brushColor)
                while (y < yend):
                    y = y + 1
                    if p < 0:
                        p = p + dx_2
                    else:
                        x = x + 1
                        p = p + dxsdy_2
                    drawPixel(x, y, canvas, id, brushColor)
            elif m == 1:
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas, id, brushColor)
                while (x < xend):
                    x = x + 1
                    y = y + 1
                    drawPixel(x, y, canvas, id, brushColor)
            elif (m>0) and (m<1):
                p = 2 * dy - dx
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas, id, brushColor)
                while (x < xend):
                    x = x + 1
                    if p < 0:
                        p = p + dy_2
                    else:
                        y = y + 1
                        p = p + dysdx_2
                    drawPixel(x, y, canvas, id, brushColor)
            elif (m > -1) and (m < 0):
                p = 2 * dy - dx
                if xstart < xend:
                    x = xend
                    y = yend
                    xend = xstart
                else: 
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas, id, brushColor)
                while (x > xend):
                    x = x - 1
                    if p < 0:
                        p = p + dy_2
                    else:
                        y = y + 1
                        p = p + dysdx_2
                    drawPixel(x,y,canvas,id, brushColor)
            elif m == -1.0:
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas,id, brushColor)
                while (x < xend):
                    x = x + 1
                    y = y - 1
                    drawPixel(x,y,canvas,id, brushColor)
            elif m < -1:
                p = 2*dx-dy
                if ystart < yend:
                    x = xend
                    y = yend
                    yend = ystart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas,id, brushColor)
                while (y > yend):
                    y = y - 1
                    if p < 0:
                        p = p + dx_2
                    else:
                        x = x + 1
                        p = p + dxsdy_2
                    drawPixel(x,y,canvas,id, brushColor)
            else:
                #print("hi")
                if (xstart == xend):
                    y = min(ystart, yend)
                    x = xstart
                    for i in range(dy):
                        drawPixel(x,y,canvas,id, brushColor)
                        y = y + 1
                elif ystart == yend:
                    x = min(xstart, xend)
                    y = ystart
                    for i in range(dx):
                        drawPixel(x,y,canvas,id, brushColor)
                        x = x + 1
         
    except ValueError:
        pass

def drawPolygon(id, vertices, algorithm, canvas):
    ''' id: unique identity for each primitive
    n: number of vertices
    vertices: list of float tuples, denotes the polygon vertices
    algorithm: string, denotes drawing algorithm
    '''
    try:
        for i in range(len(vertices)-1):
            drawLine(id, vertices[i], vertices[i+1], algorithm, canvas)
    except ValueError:
        pass

def drawEllipse(id, center, r, canvas, algorithm):
    ''' id: unique identity for each primitive
    center: float tuple, denotes the center's coordinate
    r: float tuple, (major semi-axis, minor semi-axis)
    '''
    try:
        print("Ellipse {} at center{}, radius{} using Algorithm {}".format(id, center, r, algorithm))
        (a, b) = r
        x = 0
        y = b
        if (algorithm=="MidPointCircle"):
            d1 = b*b + a*a*(0.25-b)
            while (b*b*(x+1) < a*a*(y-0.5)):
                drawPixel(center[0]+x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]-y, canvas, id, brushColor)
                drawPixel(center[0]+x, center[1]-y, canvas, id, brushColor)
                if (d1 < 0):
                    d1 = d1 + b*b*(2*x+3)
                    x = x + 1
                else:
                    d1 = d1 + b * b *(2*x+3)+a*a*(2-2*y)
                    x = x + 1
                    y = y - 1
            d2 = (b*(x+0.5))**2+(a*(y-1))**2 - (a*b)**2
            while y >= 0:
                drawPixel(center[0]+x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]-y, canvas, id, brushColor)
                drawPixel(center[0]+x, center[1]-y, canvas, id, brushColor)
                if d2 < 0:
                    d2 = d2 + b*b*(2*x+2) + a*a*(3-2*y)
                    x = x + 1
                    y = y - 1
                else:
                    d2 = d2 + a*a*(3-2*y)
                    y = y - 1
        if (algorithm=="Bresenham"):
            #print("Bresenham")
            d = b*b + a*a*(0.25-b)
            fx = int(a*a / np.sqrt(float(a*a + b*b)))
            while (x<=fx):
                if d<0:
                    d = d + b*b*(2*x+3)
                else:
                    d = d + b*b*(2*x+3)+a*a*(2-2*y)
                    y = y - 1
                x = x + 1        
                drawPixel(center[0]+x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]-y, canvas, id, brushColor)
                drawPixel(center[0]+x, center[1]-y, canvas, id, brushColor)
            #print("Yes")
            d = b*b*(x+0.5)*(x+0.5)+a*a*(y-1)*(y-1)-a*a*b*b  
            while (y>0):
                if d < 0:
                    d = d + b*b*(2*x+2) + a*a*(3-2*y)
                    x = x + 1
                else:
                    d = d + a*a*(3-2*y)
                y = y - 1
                drawPixel(center[0]+x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]+y, canvas, id, brushColor)
                drawPixel(center[0]-x, center[1]-y, canvas, id, brushColor)
                drawPixel(center[0]+x, center[1]-y, canvas, id, brushColor)
    except ValueError:
        pass

def bspline(cv, n=5000, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree,1,degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree,1,count-1)


    # Calculate knot vector
    kv = None
    if periodic:
        kv = np.arange(0-degree,count+degree+degree-1,dtype='int')
    else:
        kv = np.concatenate(([0]*degree, np.arange(count-degree+1), [count-degree]*degree))


    # Calculate query range
    u = np.linspace(periodic,(count-degree),n)


    # Calculate result
    return np.array(si.splev(u, (kv,cv.T,degree))).T

def drawCurve(id, points, algorithm, canvas):
    ''' id: unique identity for each primitive
    n: int, number of points observed on the curve
    points: list of float tuples, denotes n observed points coordinate
    algorithm: string, denotes drawing algorithm
    '''
    try:
        if (algorithm == "Bezier"):
            points = np.array(points)
            NumPoint = len(points)-1
            t = np.arange(0,1,0.001)
            x = np.power((1-t),NumPoint)*points[0][0]
            y = np.power((1-t),NumPoint)*points[0][1]
            #print(t, x, y)
            for i in range(NumPoint):
                part1 = np.power((1-t),(NumPoint-i-1))
                part2 = np.power(t, i+1)
                param = factorial(NumPoint)/(factorial(i+1)*factorial(NumPoint-i-1)) 
                w = np.multiply(part1, part2) * param
                #print(part1, part2, param, w)
                #print(points[:,0])
                x = x + np.multiply(w, points[i+1,0])
                #print(x)
                y = y + np.multiply(w, points[i+1,1])
                #print(y)
            for i in range(len(x)):
                drawPixel(x[i],y[i], canvas, id, brushColor)
        if (algorithm == "B-spline"):
            if Manhattan(points[0],points[len(points)-1]) <=8:
                points.pop()
                #points.append(points[0])
                points = np.array(points)
                result = bspline(points, periodic=True)
            else:
                points = np.array(points)
                result = bspline(points)
            for i in result:
                drawPixel(i[0],i[1],canvas, id, brushColor)
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
