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

def drawPixel(x, y, canvas, id, brushColor):
    variable = canvas.create_rectangle(x, y, x, y, outline=brushColor)
    if id != -1:
        Objects.xyList[id].append((x,y,brushColor))
        Objects.obList[id].append(variable)
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
        Objects.obList.clear()  
        canvas.delete("all")  
        Objects.ObjectId = -1
        Objects.obList.append([]) 
        Objects.xyList.clear()
        Objects.xyList.append([])
        Objects.missionList.clear()
        width = int(width.get())
        height = int(height.get())
        print(width, height, type(width), type(height))
        canvas.bind("<Configure>")
        canvas.width = width
        canvas.height = height
        canvas.config(width = canvas.width, height=canvas.height)
        canvas.pack(fill=BOTH, expand=YES)
        Objects.image=Image.new("RGB",(canvas.width,canvas.height),(255,255,255))
        
    except ValueError:
        pass

def saveCanvas(name, canvas):
    '''save current canvas as name.bmp, 
    name: string
    '''
    canvas.update()
    name = name.get()
    canvas.bind("<Configure>")
    Objects.image = Image.new("RGB",(canvas.width,canvas.height),(255,255,255))
    print("name = {}".format(name))
    canvas.postscript(file="{}.eps".format(name),colormode='color')
    for i in Objects.xyList:
        for j in i:
            drawImagePixel(j[0],j[1],j[2])
    Objects.image.save(name+'.bmp')

    
def setColor(R, G, B, canvas):
    '''set brush color, 
    0 <= R, G, B <= 255
    '''
    try:
        r, g, b = int(R.get()), int(G.get()), int(B.get())
        print(r,type(r),g,type(g),b,type(b))
        r_str = hex(r).lstrip("0x")
        g_str = hex(g).lstrip("0x")
        b_str = hex(b).lstrip("0x")
        if (r_str == ""):
            r_str = "00"
        if (g_str == ""):
            g_str = "00"
        if (b_str == ""):
            b_str = "00"
        print(r_str, g_str, b_str)
        Objects.brushColor = "#"+r_str+g_str+b_str
        print(Objects.brushColor)
    except ValueError:
        pass

def drawLine(id, p1, p2, algorithm, canvas, brushColor): 
    ''' id: unique identity for each primitive
     p1, p2: float tuples, denote the startpoint and endpoint coordinates
     algorithm: string, denotes drawing algorithm, eg:DDA or bresenham
     '''
    try:
        Objects.missionList.append(["line", id, p1, p2, algorithm, brushColor])
        print("drawcolor=",Objects.brushColor)
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
        canvas.update()  
    except ValueError:
        pass

def drawPolygon(id, vertices, algorithm, canvas, brushColor):
    ''' id: unique identity for each primitive
    n: number of vertices
    vertices: list of float tuples, denotes the polygon vertices
    algorithm: string, denotes drawing algorithm
    '''
    try:
        print(id, type(id))
        Objects.missionList.append(["polygon",id, vertices, algorithm,brushColor])
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
        Objects.missionList.append(["ellipse", id, center, r, algorithm, brushColor])
        #brushColor = Objects.brushColor
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

def drawCurve(id, points, algorithm, canvas, brushColor):
    ''' id: unique identity for each primitive
    n: int, number of points observed on the curve
    points: list of float tuples, denotes n observed points coordinate
    algorithm: string, denotes drawing algorithm
    '''
    try:
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
        obTarget = Objects.obList[id]
        xyTarget = Objects.xyList[id]
        length = len(obTarget)
        for i in range(length):
            ob = obTarget.pop(0)
            xy = xyTarget.pop(0)
            canvas.delete(ob)
            x = xy[0]+d[0]
            y = xy[1]+d[1]
            brushColor = xy[2]
            variable = canvas.create_rectangle(x, y, x, y, outline=brushColor)
            obTarget.append(variable)
            xyTarget.append((x,y,brushColor))
        print(id, d)
    except ValueError:
        pass

def rotate(id, center, r, canvas):
    ''' id: unique identity for each primitive
    center = (x, y): float tuple, denotes the rotation center coordinate
    r: float, the angle of clockwise rotation
    '''
    try:
        obTarget = Objects.obList[id]
        xyTarget = Objects.xyList[id]
        length = len(obTarget)
        for i in range(length):
            ob = obTarget.pop(0)
            xy = xyTarget.pop(0)
            canvas.delete(ob)
            dx = xy[0]-center[0]
            dy = xy[1]-center[1]
            x = center[0]+np.cos(r)*dx-np.sin(r)*dy
            y = center[1]+np.sin(r)*dx+np.cos(r)*dy
            brushColor = xy[2]
            variable = canvas.create_rectangle(x, y, x, y, outline=brushColor)
            obTarget.append(variable)
            xyTarget.append((x,y,brushColor))
        print(id, center, r)
    except ValueError:
        pass

def scale(id, center, s, canvas):
    ''' id: unique identity for each primitive
    center = (x,y): float tuple, denotes the coordinate of scaling center
    s: float, denotes scale of scaling
    '''
    try:
        obTarget = Objects.obList[id]
        xyTarget = Objects.xyList[id]
        length = len(obTarget)
        for i in range(length):
            ob = obTarget.pop(0)
            xy = xyTarget.pop(0)
            canvas.delete(ob)
        obTarget.clear()
        xyTarget.clear()
        missionTarget = Objects.missionList[id]
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
        
            
        print(id,center,s)
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

def liangBarskyClip(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    

def clip(id, p1, p2, algorithm, canvas):
    ''' id: unique identity for each primitive
    p1, p2: float tuples, denote up-left and down-right coordinate of target window
    algorithm: string, denotes the clipping algorithm.
    '''
    try:
        if Objects.missionList[id][0] != "line":
            print("The clip target is not a line, please select a new target!")
            return 
        x1, y1 = Objects.missionList[id][2]
        x2, y2 = Objects.missionList[id][3]
        brushColor = Objects.missionList[id][5]
        if algorithm == "Cohen–Sutherland":
            new_x1, new_y1, new_x2, new_y2 = cohenSutherlandClip(x1, y1, x2, y2, p1[0], p2[0], p1[1], p2[1])
        elif algorithm == "Liang-Barsky":
            return 
        else:
            print("Wrong Algorithm for Clipping")
            return 
        for i in Objects.obList[id]:
            canvas.delete(i)
        Objects.obList[id].clear()
        Objects.xyList[id].clear()
        new_x1, new_y1, new_x2, new_y2 = int(new_x1), int(new_y1), int(new_x2), int(new_y2)
        drawLine(id, (new_x1,new_y1),(new_x2,new_y2), Objects.missionList[id][4], canvas, brushColor)
        targetMission = Objects.missionList.pop()
        Objects.missionList[id].clear()
        while (targetMission):
            Objects.missionList[id].append(targetMission.pop(0))
        print(id,p1,p2,algorithm)
    except ValueError:
        pass
