from tkinter import *
from tkinter import ttk
from Objects import Objects
import numpy as np
from math import *
import scipy.interpolate as si
import io
from PIL import Image, ImageDraw
import os

__author__ = 'Jing Tan'

def findId(id):
    for i in range(len(Objects.missionList)):
        if Objects.missionList[i][1] == id:
            return i


def drawPixel(x, y, canvas, id, brushColor):
    if canvas:
        variable = canvas.create_rectangle(x, y, x, y, outline=brushColor)
    if id != -1:
        index = findId(id)
        if canvas:
            Objects.obList[index].append(variable)
        #print(index, Objects.missionList)
        Objects.xyList[index].append((x,y,brushColor))
    if canvas:
        return variable  

def drawImagePixel(x,y,brushColor):
    draw = ImageDraw.Draw(Objects.image)
    draw.point((x,y,x,y),fill=brushColor)

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
        Objects.xyList.clear()
        Objects.xyList.append([])
        Objects.missionList.clear()
        #Objects.idList.clear()
        if width and height:
            width = int(width)
            height = int(height)
            #print(width, height, type(width), type(height))
        else:
            width, height = Objects.width, Objects.height
        if canvas:
            Objects.obList.clear()  
            Objects.obList.append([]) 
            Objects.ObjectId = -1
            canvas.delete("all")  
        Objects.image=Image.new("RGB",(width,height),(255,255,255))
        Objects.width = width
        Objects.height = height
        
    except ValueError:
        pass

def saveCanvas(name, canvas):
    '''save current canvas as name.bmp, 
    name: string
    '''
    Objects.image = Image.new("RGB",(Objects.width,Objects.height),(255,255,255))
    #print("name = {}".format(name))
    for i in Objects.xyList:
        for j in i:
            drawImagePixel(j[0],j[1],j[2])
    Objects.image.save(name+'.bmp')
  
def setColor(R, G, B, canvas):
    '''set brush color, 
    0 <= R, G, B <= 255
    '''
    try:
        r, g, b = int(R), int(G), int(B)
        #print(r,type(r),g,type(g),b,type(b))
        r_str = hex(r).lstrip("0x")
        g_str = hex(g).lstrip("0x")
        b_str = hex(b).lstrip("0x")
        if (r_str == ""):
            r_str = "00"
        if (g_str == ""):
            g_str = "00"
        if (b_str == ""):
            b_str = "00"
        #print(r_str, g_str, b_str)
        Objects.brushColor = "#"+r_str+g_str+b_str
        #print(Objects.brushColor)
    except ValueError:
        pass

def drawLine(id, p1, p2, algorithm, canvas, brushColor): 
    ''' id: unique identity for each primitive
     p1, p2: float tuples, denote the startpoint and endpoint coordinates
     algorithm: string, denotes drawing algorithm, eg:DDA or bresenham
     '''
    try:
        Objects.xyList.append([])
        Objects.missionList.append(["line", id, p1, p2, algorithm, brushColor])
        #Objects.idList.append(id)
        #print("drawcolor=",Objects.brushColor)
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
                drawPixel(int(x), int(y), canvas, id,brushColor)
        

        elif (algorithm=="Bresenham"):
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
                drawPixel(x, y, canvas, id,brushColor)
                while (y < yend):
                    y = y + 1
                    if p < 0:
                        p = p + dx_2
                    else:
                        x = x + 1
                        p = p + dxsdy_2
                    drawPixel(x, y, canvas, id,brushColor)
            elif m == 1:
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas, id,brushColor)
                while (x < xend):
                    x = x + 1
                    y = y + 1
                    drawPixel(x, y, canvas, id,brushColor)
            elif (m>0) and (m<1):
                p = 2 * dy - dx
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x, y, canvas, id,brushColor)
                while (x < xend):
                    x = x + 1
                    if p < 0:
                        p = p + dy_2
                    else:
                        y = y + 1
                        p = p + dysdx_2
                    drawPixel(x, y, canvas, id,brushColor)
            elif (m > -1) and (m < 0):
                p = 2 * dy - dx
                if xstart < xend:
                    x = xend
                    y = yend
                    xend = xstart
                else: 
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas, id,brushColor)
                while (x > xend):
                    x = x - 1
                    if p < 0:
                        p = p + dy_2
                    else:
                        y = y + 1
                        p = p + dysdx_2
                    drawPixel(x,y,canvas,id,brushColor)
            elif m == -1.0:
                if xstart > xend:
                    x = xend
                    y = yend
                    xend = xstart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas,id,brushColor)
                while (x < xend):
                    x = x + 1
                    y = y - 1
                    drawPixel(x,y,canvas,id,brushColor)
            elif m < -1:
                p = 2*dx-dy
                if ystart < yend:
                    x = xend
                    y = yend
                    yend = ystart
                else:
                    x = xstart
                    y = ystart
                drawPixel(x,y,canvas,id,brushColor)
                while (y > yend):
                    y = y - 1
                    if p < 0:
                        p = p + dx_2
                    else:
                        x = x + 1
                        p = p + dxsdy_2
                    drawPixel(x,y,canvas,id,brushColor)
            else:
                #print("hi")
                if (xstart == xend):
                    y = min(ystart, yend)
                    x = xstart
                    for i in range(dy):
                        drawPixel(x,y,canvas,id,brushColor)
                        y = y + 1
                elif ystart == yend:
                    x = min(xstart, xend)
                    y = ystart
                    for i in range(dx):
                        drawPixel(x,y,canvas,id,brushColor)
                        x = x + 1 
        else:
            print("Wrong Algorithm for Line/Polygon!")
            #Objects.ObjectId = Objects.ObjectId - 1
    except ValueError:
        pass

def drawPolygon(id, vertices, algorithm, canvas, brushColor):
    ''' id: unique identity for each primitive
    n: number of vertices
    vertices: list of float tuples, denotes the polygon vertices
    algorithm: string, denotes drawing algorithm
    '''
    try:
        Objects.xyList.append([])
        #print(id, type(id))
        Objects.missionList.append(["polygon",id, vertices, algorithm,brushColor])
        #Objects.idList.append(id)
        for i in range(len(vertices)-1):
            drawLine(id, vertices[i], vertices[i+1], algorithm, canvas, brushColor=brushColor)
            Objects.missionList.pop()
        drawLine(id, vertices[len(vertices)-1], vertices[0], algorithm, canvas, brushColor=brushColor)
        Objects.missionList.pop()
    except ValueError:
        pass

def drawEllipse(id, center, r, canvas, algorithm, brushColor):
    ''' id: unique identity for each primitive
    center: float tuple, denotes the center's coordinate
    r: float tuple, (major semi-axis, minor semi-axis)
    '''
    try:
        Objects.xyList.append([])
        Objects.missionList.append(["ellipse", id, center, r, algorithm, brushColor])
        #brushColor = Objects.brushColor
        #print("Ellipse {} at center{}, radius{} using Algorithm {}".format(id, center, r, algorithm))
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
        elif (algorithm=="Bresenham"):
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
        else: 
            print("Wrong Algorithm for Ellipse!")
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

def drawCurve(id, points, algorithm, canvas, brushColor):
    ''' id: unique identity for each primitive
    n: int, number of points observed on the curve
    points: list of float tuples, denotes n observed points coordinate
    algorithm: string, denotes drawing algorithm
    '''
    try:
        Objects.xyList.append([])
        Objects.missionList.append(["curve", id, points, algorithm,brushColor])
        #brushColor = Objects.brushColor
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
        elif (algorithm == "B-spline"):
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
        else:
            print("Wrong Algorithm to draw Curve!")
    except ValueError:
        pass

def translate(id, d, canvas):
    ''' id: unique identity for each primitive
    d: float tuple, denotes the translation vector
    '''
    try:
        index = findId(id)
        if canvas:
            obTarget = Objects.obList[index]
        xyTarget = Objects.xyList[index]
        length = len(xyTarget)
        for i in range(length):
            if canvas: 
                ob = obTarget.pop(0)
                canvas.delete(ob)
            xy = xyTarget.pop(0)
        if canvas: 
            obTarget.clear()
        xyTarget.clear()
        missionTarget = Objects.missionList[index]
        if missionTarget[0] == "line":
            p1 = missionTarget[2]
            p2 = missionTarget[3]
            new_p1 = p1[0]+d[0], p1[1]+d[1]
            new_p2 = p2[0]+d[0], p2[1]+d[1]
            new_p1 = int(new_p1[0]), int(new_p1[1])
            new_p2 = int(new_p2[0]), int(new_p2[1])
            drawLine(missionTarget[1], new_p1, new_p2, missionTarget[4], canvas, brushColor=missionTarget[5])
        if missionTarget[0] == 'polygon':
            vertices = missionTarget[2]
            new_vertices = []
            for i in vertices:
                new_i = i[0]+d[0], i[1]+d[1]
                new_i = int(new_i[0]),int(new_i[1])
                new_vertices.append(new_i)
            drawPolygon(missionTarget[1], new_vertices, missionTarget[3], canvas, brushColor=missionTarget[4])
        if missionTarget[0] == 'ellipse':
            center_e = missionTarget[2]
            center_e = center_e[0]+d[0], center_e[1]+d[1]
            drawEllipse(missionTarget[1],center_e, missionTarget[3], canvas, missionTarget[4], brushColor=missionTarget[5])
        if missionTarget[0] == 'curve':
            points = missionTarget[2]
            new_points = []
            for i in points:
                new_i = i[0]+d[0], i[1]+d[1]
                new_i = int(new_i[0]),int(new_i[1])
                new_points.append(new_i)
            drawCurve(missionTarget[1], new_points, missionTarget[3], canvas,brushColor= missionTarget[4])
        target = Objects.missionList.pop()
        missionTarget.clear()
        while (target):
            missionTarget.append(target.pop(0))
    except ValueError:
        pass

def rotate(id, center, r, canvas):
    ''' id: unique identity for each primitive
    center = (x, y): float tuple, denotes the rotation center coordinate
    r: float, the angle of clockwise rotation
    '''
    try:
        index = findId(id)
        if canvas:
            obTarget = Objects.obList[index]
        xyTarget = Objects.xyList[index]
        length = len(xyTarget)
        for i in range(length):
            if canvas: 
                ob = obTarget.pop(0)
                canvas.delete(ob)
            xy = xyTarget.pop(0)
        if canvas: 
            obTarget.clear()
        xyTarget.clear()
        missionTarget = Objects.missionList[index]
        if missionTarget[0] == "line":
            p1 = missionTarget[2]
            p2 = missionTarget[3]
            dx = (p1[0]-center[0])
            dy = (p1[1]-center[1])
            new_p1 = center[0]+np.cos(r)*dx-np.sin(r)*dy, center[1]+np.sin(r)*dx+np.cos(r)*dy
            dx = (p2[0]-center[0])
            dy = (p2[1]-center[1])
            new_p2 = center[0]+np.cos(r)*dx-np.sin(r)*dy, center[1]+np.sin(r)*dx+np.cos(r)*dy
            new_p1 = int(new_p1[0]), int(new_p1[1])
            new_p2 = int(new_p2[0]), int(new_p2[1])
            drawLine(missionTarget[1], new_p1, new_p2, missionTarget[4], canvas, brushColor=missionTarget[5])
        if missionTarget[0] == 'polygon':
            vertices = missionTarget[2]
            new_vertices = []
            for i in vertices:
                dx = (i[0]-center[0])
                dy = (i[1]-center[1])
                new_i = center[0]+np.cos(r)*dx-np.sin(r)*dy, center[1]+np.sin(r)*dx+np.cos(r)*dy
                new_i = int(new_i[0]),int(new_i[1])
                new_vertices.append(new_i)
            drawPolygon(missionTarget[1], new_vertices, missionTarget[3], canvas, brushColor=missionTarget[4])
        if missionTarget[0] == 'ellipse':
            center_e = missionTarget[2]
            dx = center_e[0] - center[0]
            dy = center_e[1] - center[1]
            center_e = center[0]+np.cos(r)*dx-np.sin(r)*dy, center[1]+np.sin(r)*dx+np.cos(r)*dy
            drawEllipse(missionTarget[1],center_e, missionTarget[3], canvas, missionTarget[4], brushColor=missionTarget[5])
        if missionTarget[0] == 'curve':
            points = missionTarget[2]
            new_points = []
            for i in points:
                dx = (i[0]-center[0])
                dy = (i[1]-center[1])
                new_i = center[0]+np.cos(r)*dx-np.sin(r)*dy, center[1]+np.sin(r)*dx+np.cos(r)*dy
                new_i = int(new_i[0]),int(new_i[1])
                new_points.append(new_i)
            drawCurve(missionTarget[1], new_points, missionTarget[3], canvas,brushColor= missionTarget[4])
        target = Objects.missionList.pop()
        missionTarget.clear()
        while (target):
            missionTarget.append(target.pop(0))
        
        #print(id, center, r)
    except ValueError:
        pass

def scale(id, center, s, canvas):
    ''' id: unique identity for each primitive
    center = (x,y): float tuple, denotes the coordinate of scaling center
    s: float, denotes scale of scaling
    '''
    try:
        index = findId(id)
        if canvas:
            obTarget = Objects.obList[index]
        xyTarget = Objects.xyList[index]
        length = len(xyTarget)
        for i in range(length):
            if canvas: 
                ob = obTarget.pop(0)
                canvas.delete(ob)
            xy = xyTarget.pop(0)
        if canvas: 
            obTarget.clear()
        xyTarget.clear()
        missionTarget = Objects.missionList[index]
        if missionTarget[0] == "line":
            p1 = missionTarget[2]
            p2 = missionTarget[3]
            new_p1 = (p1[0]-center[0])*s+center[0], (p1[1]-center[1])*s+center[1]
            new_p2 = (p2[0]-center[0])*s+center[0], (p2[1]-center[1])*s+center[1]
            new_p1 = int(new_p1[0]), int(new_p1[1])
            new_p2 = int(new_p2[0]), int(new_p2[1])
            drawLine(missionTarget[1], new_p1, new_p2, missionTarget[4], canvas, brushColor=missionTarget[5])
        if missionTarget[0] == 'polygon':
            vertices = missionTarget[2]
            new_vertices = []
            for i in vertices:
                new_i = (i[0]-center[0])*s+center[0], (i[1]-center[1])*s+center[1]
                new_i = int(new_i[0]),int(new_i[1])
                new_vertices.append(new_i)
            drawPolygon(missionTarget[1], new_vertices, missionTarget[3], canvas, brushColor=missionTarget[4])
        if missionTarget[0] == 'ellipse':
            r = missionTarget[3]
            new_r = r[0]*s, r[1]*s
            drawEllipse(missionTarget[1], missionTarget[2], new_r, canvas, missionTarget[4], brushColor=missionTarget[5])
        if missionTarget[0] == 'curve':
            points = missionTarget[2]
            new_points = []
            for i in points:
                new_i = (i[0]-center[0])*s+center[0], (i[1]-center[1])*s+center[1]
                new_i = int(new_i[0]),int(new_i[1])
                new_points.append(new_i)
            drawCurve(missionTarget[1], new_points, missionTarget[3], canvas,brushColor= missionTarget[4])
        target = Objects.missionList.pop()
        missionTarget.clear()
        while (target):
            missionTarget.append(target.pop(0))
        
            
        #print(id,center,s)
    except ValueError:
        pass
# Defining region codes 
INSIDE = 0  #0000 
LEFT = 1    #0001 
RIGHT = 2   #0010 
BOTTOM = 4  #0100 
TOP = 8     #1000 
# Function to compute region code for a point(x,y) 
def computeCode(x, y, x_min, x_max, y_min, y_max): 
    code = INSIDE 
    if x < x_min:      # to the left of rectangle 
        code |= LEFT 
    elif x > x_max:    # to the right of rectangle 
        code |= RIGHT 
    if y < y_min:      # below the rectangle 
        code |= BOTTOM 
    elif y > y_max:    # above the rectangle 
        code |= TOP 
    return code  
# Implementing Cohen-Sutherland algorithm 
# Clipping a line from P1 = (x1, y1) to P2 = (x2, y2) 
# https://www.geeksforgeeks.org/line-clipping-set-1-cohen-sutherland-algorithm/
def cohenSutherlandClip(x1, y1, x2, y2, x_min, x_max, y_min, y_max): 
    # Compute region codes for P1, P2 
    code1 = computeCode(x1, y1, x_min, x_max, y_min, y_max) 
    code2 = computeCode(x2, y2, x_min, x_max, y_min, y_max) 
    accept = False
    while True: 
        # If both endpoints lie within rectangle 
        if code1 == 0 and code2 == 0: 
            accept = True
            break
        # If both endpoints are outside rectangle 
        elif (code1 & code2) != 0: 
            break
        # Some segment lies within the rectangle 
        else: 
            # Line Needs clipping 
            # At least one of the points is outside,  
            # select it 
            x = 1.0
            y = 1.0
            if code1 != 0: 
                code_out = code1 
            else: 
                code_out = code2 
            # Find intersection point 
            # using formulas y = y1 + slope * (x - x1),  
            # x = x1 + (1 / slope) * (y - y1) 
            if code_out & TOP: 
                # point is above the clip rectangle 
                x = x1 + (x2 - x1) * \
                                (y_max - y1) / (y2 - y1) 
                y = y_max 
            elif code_out & BOTTOM: 
                # point is below the clip rectangle 
                x = x1 + (x2 - x1) * \
                                (y_min - y1) / (y2 - y1) 
                y = y_min 
            elif code_out & RIGHT: 
                # point is to the right of the clip rectangle 
                y = y1 + (y2 - y1) * \
                                (x_max - x1) / (x2 - x1) 
                x = x_max 
            elif code_out & LEFT: 
                  
                # point is to the left of the clip rectangle 
                y = y1 + (y2 - y1) * \
                                (x_min - x1) / (x2 - x1) 
                x = x_min 
            # Now intersection point x,y is found 
            # We replace point outside clipping rectangle 
            # by intersection point 
            if code_out == code1: 
                x1 = x 
                y1 = y 
                code1 = computeCode(x1,y1, x_min, x_max, y_min, y_max) 
            else: 
                x2 = x 
                y2 = y 
                code2 = computeCode(x2, y2, x_min, x_max, y_min, y_max) 
    if accept: 
        print ("Line accepted from %.2f,%.2f to %.2f,%.2f" % (x1,y1,x2,y2))
        return x1,y1,x2,y2 
        # Here the user can add code to display the rectangle 
        # along with the accepted (portion of) lines  
    else: 
        print("Line rejected, completely outside the clipping area") 
        return x1,y1,x2,y2 

def clipTest(p, q, t1, t2):
    retVal = True
    if p < 0.0:
        r = q/p
        if r > t2:
            retVal = False
        elif r > t1:
            t1 = r
    elif p > 0.0:
        r = q/p
        if r < t1:
            retVal = False
        elif r < t2:
            t2 = r
    elif q < 0.0:
        retVal = False
    return retVal, t1, t2

def liangBarskyClip(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    t1, t2, dx = 0.0, 1.0, x2-x1
    flag, t1, t2 = clipTest(-dx, x1-x_min, t1, t2)
    if (flag):
        flag, t1, t2 = clipTest(dx, x_max-x1, t1, t2)
        if (flag):
            dy = y2-y1
            flag, t1, t2 = clipTest(-dy, y1-y_min, t1, t2)
            if (flag):
                flag, t1, t2 = clipTest(dy, y_max-y1, t1,t2)
                if (flag):
                    if (t2 < 1.0):
                        x2 = x1+t2*dx
                        y2 = y1+t2*dy
                    if (t1 > 0.0):
                        x1 = x1 + t1*dx
                        y1 = y1 + t1*dy
                    return int(x1), int(y1), int(x2), int(y2)
    print("Line unaccepted!")
    return 

def clip(id, p1, p2, algorithm, canvas):
    ''' id: unique identity for each primitive
    p1, p2: float tuples, denote up-left and down-right coordinate of target window
    algorithm: string, denotes the clipping algorithm.
    '''
    try:
        index = findId(id)
        if Objects.missionList[index][0] != "line":
            print("The clip target is not a line, please select a new target!")
            return
#print(Objects.missionList[index]) 
        x1, y1 = Objects.missionList[index][2]
        x2, y2 = Objects.missionList[index][3]
        brushColor = Objects.missionList[index][5]
        if algorithm == "Cohen–Sutherland":
            new_x1, new_y1, new_x2, new_y2 = cohenSutherlandClip(x1, y1, x2, y2, p1[0], p2[0], p1[1], p2[1])
        elif algorithm == "Liang-Barsky":
            new_x1, new_y1, new_x2, new_y2 = liangBarskyClip(x1, y1, x2, y2, p1[0], p2[0], p1[1], p2[1])
            #print(new_x1, new_y1, new_x2, new_y2)
        else:
            print("Wrong Algorithm for Line Clipping")
            return 
        if canvas:
            for i in Objects.obList[index]:
                canvas.delete(i)
            Objects.obList[index].clear()
        Objects.xyList[index].clear()
        new_x1, new_y1, new_x2, new_y2 = int(new_x1), int(new_y1), int(new_x2), int(new_y2)
        drawLine(id, (new_x1,new_y1),(new_x2,new_y2), Objects.missionList[index][4], canvas, brushColor)
        targetMission = Objects.missionList.pop()
        Objects.missionList[index].clear()
        while (targetMission):
            Objects.missionList[index].append(targetMission.pop(0))
        #print(index,p1,p2,algorithm)
    except ValueError:
        pass
