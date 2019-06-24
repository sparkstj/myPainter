from tkinter import *
from tkinter import ttk
import algorithms
from Objects import Objects
from PIL import Image, ImageDraw
import numpy as np

clickList = []
MotionList = []
drawLine = False
drawPolygon = False
drawEllipse = False
drawCurve = False

def Manhattan(p0, p1):
	(x0, y0) = p0
	(x1, y1) = p1
	return abs(x1-x0)+abs(y1-y0)

def LineSignal():
	global drawLine 
	Objects.ObjectId = Objects.ObjectId + 1
	Objects.obList.append([])
	#Objects.xyList.append([])
	print(Objects.ObjectId)
	drawLine = True
	clickList.clear()
	
def PolygonSignal():
	global drawPolygon
	drawPolygon = True
	Objects.ObjectId = Objects.ObjectId + 1
	Objects.obList.append([])
	#Objects.xyList.append([])
	#print(ObjectId)
	clickList.clear()

def EllipseSignal():
	try:
		#print("ellipse")
		global w
		global algorithm
		Objects.ObjectId = Objects.ObjectId + 1
		Objects.obList.append([])
		##Objects.xyList.append([])
		leftup = MotionList[0]
		rightdown = MotionList[len(MotionList)-1]
		center = (int((leftup[0]+rightdown[0])/2), int((leftup[1]+rightdown[1])/2))
		longradius = int(abs(leftup[0]-rightdown[0])/2)
		shortradius = int(abs(leftup[1]-rightdown[1])/2)
		print("Ellipse {} with center {}, radius {} using Algorithm {}".format(Objects.ObjectId,center, (longradius, shortradius),algorithm.get()))
		algorithms.drawEllipse(Objects.ObjectId, center, (longradius, shortradius), w, algorithm.get(), Objects.brushColor)
		MotionList.clear()
		clickList.clear()
	except:
		Objects.ObjectId = Objects.ObjectId - 1
		print("please select the ellipse district first")
		
def CurveSignal():
	global drawCurve
	global w
	global algorithm
	Objects.ObjectId = Objects.ObjectId + 1
	Objects.obList.append([])
	##Objects.xyList.append([])
	drawCurve = True
	#print(Objects.ObjectId)
	if (len(clickList)>=2): #Curve Control Points should be selected before clicking the button
		print("Curve {} with control points {} using Algorithm {}".format(Objects.ObjectId,clickList,algorithm.get()))
		algorithms.drawCurve(Objects.ObjectId, clickList.copy(), algorithm.get(), w, Objects.brushColor)
		clickList.clear()
		drawCurve = False
	clickList.clear()

def TranslateSignal(id):
	global w
	global algorithm
	id = int(id)
	p1 = MotionList[0]
	p2 = MotionList[len(MotionList)-1]
	MotionList.clear()
	algorithms.translate(id,(p2[0]-p1[0],p2[1]-p1[1]),w)

def RotateSignal(id): #must select angle then select points before rotate (sequence is important)
	global w
	global algorithm
	id = int(id)
	center = clickList.pop()
	p1 = MotionList[0]
	p2 = MotionList[len(MotionList)-1]
	MotionList.clear()
	dx1 = p1[0]-center[0]
	dy1 = p1[1]-center[1]
	dx2 = p2[0]-center[0]
	dy2 = p2[1]-center[1]
	if dx1 == 0:
		r1 = 90*3.14/180
	else:
		r1 = np.arctan(dy1/dx1)
	if dx2 == 0:
		r2 = 90*3.14/180
	else:
		r2 = np.arctan(dy2/dx2)
	r = r2-r1
	algorithms.rotate(id, center, r, w)

def ScaleSignal(id, s):
	global w
	global algorithm
	id = int(id)
	s = float(s)
	center = clickList.pop()
	algorithms.scale(id, center, s, w)

def ClipSignal(id):
	global w
	global algorithm
	id = int(id)
	leftup = MotionList[0]
	rightdown = MotionList[len(MotionList)-1]
	algorithms.clip(id, leftup, rightdown, algorithm.get(),w)

def drag( event):
	MotionList.append((event.x, event.y))
	
def paint( event ):
	global algorithm
	global w
	global drawLine
	global drawPolygon
	global drawCurve
	x, y = event.x, event.y
	#print(Objects.brushColor)
	variable = algorithms.drawPixel(x, y, w, -1, Objects.brushColor)
	#print(drawCurve)
	if (drawLine == True) or (drawPolygon == True):
		Objects.obList[Objects.ObjectId].append(variable)
		Objects.xyList[Objects.ObjectId].append((x,y,Objects.brushColor))
	clickList.append((x,y))
	if (drawLine == True )and(len(clickList)>=2):
		End = clickList.pop()
		Start = clickList.pop()
		clickList.clear()
		algorithms.drawLine(Objects.ObjectId, Start, End, algorithm.get(), w, Objects.brushColor)
		print("Line {} from {} to {}, using Algorithm {}".format(Objects.ObjectId, Start, End, algorithm.get()))
		drawLine = False
	if (drawPolygon == True) and (len(clickList)>=2):
		if (Manhattan(clickList[0], (x,y)) < 8): 
			print("Polygon {} using Algorithm {}".format(Objects.ObjectId,algorithm.get()))
			algorithms.drawLine(Objects.ObjectId, clickList[len(clickList)-2],clickList[0], algorithm.get(), w, Objects.brushColor)
			Objects.missionList.pop()
			clickList.pop()
			Objects.missionList.append(["polygon",Objects.ObjectId, clickList.copy(), algorithm.get(), Objects.brushColor])
			clickList.clear()
			#drawPolygon = False
			#Objects.obList.append([])
			drawPolygon = False
		else:
			algorithms.drawLine(Objects.ObjectId, clickList[len(clickList)-2],clickList[len(clickList)-1], algorithm.get(), w ,Objects.brushColor)
			Objects.missionList.pop()

def Clean():
	print("clean")
	for i in Objects.obList[1]:
		w.delete(i)
	Objects.obList.pop(1)
	#for j in Objects.obList:
	#	for i in j:
	#		algorithms.drawPixel(i[0],i[1],w,-1,Objects.brushColor)
	

def gui():
	global algorithm
	global w
	Panel = Tk()
	Panel.columnconfigure(0, weight=1)
	Panel.rowconfigure(0, weight=1)
	w = Canvas(Panel, 
    	       width=Objects.width, 
        	   height=Objects.height,background="white")
	w.grid(column=0, row=1)
	w.bind("<Button-1>", paint)
	w.bind( "<B1-Motion>", drag )

	PanelFrame = ttk.Frame(Panel)
	PanelFrame.grid(column=0, row=0, sticky="n")
	Panel.title("Painter")
	algorithm_label = Label(PanelFrame, text='Algorithm:').grid(column=1,row=0,sticky=W)
	algorithm = StringVar(Panel)
	option = ["DDA","Bresenham","MidPointCircle","Bezier","B-spline","Cohen–Sutherland","Liang-Barsky"]
	algorithm.set(option[0])
	#print(algorithm.get())
	algorithm_om = OptionMenu(PanelFrame, algorithm, *option)
	algorithm_om.grid(column=2,row=0,sticky=W)

	LineButton1 = Button(PanelFrame, text="Draw Line", command= LineSignal ).grid(column=3, row=0, sticky=W)
	PolygonButton = Button(PanelFrame, text="Draw Polygon", command=PolygonSignal).grid(column=4, row=0, sticky=W)
	EllipseButton = Button(PanelFrame, text="Draw Ellipse", command=EllipseSignal).grid(column=5, row=0, sticky=W)
	CurveButton = Button(PanelFrame, text="Draw Curve", command=CurveSignal).grid(column=6, row=0, sticky=W)
	name_label = Label(PanelFrame, text="name:").grid(column=2, row=5, sticky=W)
	name_entry = Entry(PanelFrame)
	name_entry.grid(column=3,row=5,sticky=W)
	name_entry.focus_set()
	name_button = Button(PanelFrame, text="Save Canvas", command = lambda: algorithms.saveCanvas(name_entry.get(), w)).grid(column=1,	row=5,sticky=W)
	reset_button = Button(PanelFrame, text='Reset Canvas', command = lambda: algorithms.resetCanvas(None, None, w)).grid(column=7,row=0,sticky=W)
	r_label = Label(PanelFrame, text="R:", justify=CENTER).grid(column=2,row=7,sticky=W)
	r_entry = Entry(PanelFrame)
	r_entry.grid(column=3,row=7,sticky=W)
	g_label = Label(PanelFrame, text="G:", justify=CENTER).grid(column=4,row=7,sticky=W)
	g_entry = Entry(PanelFrame)
	g_entry.grid(column=5,row=7,sticky=W)
	b_label = Label(PanelFrame, text="B:").grid(column=6,row=7,sticky=W)
	b_entry = Entry(PanelFrame)
	b_entry.grid(column=7,row=7,sticky=W)
	rgb_button = Button(PanelFrame, text="Set Color", command= lambda: algorithms.setColor(r_entry.get(),g_entry.get(),b_entry.get(),w)).grid(column=1,row=7,sticky=W)
	translate_button = Button(PanelFrame, text="Translate", command=lambda: TranslateSignal(id_entry.get())).grid(column=1,row=8,sticky=W)
	rotate_button = Button(PanelFrame, text="Rotate", command=lambda: RotateSignal(id_entry.get())).grid(column=2,row=8,sticky=W)
	scale_button = Button(PanelFrame, text="Scale", command=lambda: ScaleSignal(id_entry.get(), scale_entry.get())).grid(column=3,row=8,sticky=W)
	clip_button = Button(PanelFrame, text="Clip", command=lambda: ClipSignal(id_entry.get())).grid(column=4,row=8,sticky=W)
	id_label = Label(PanelFrame, text="Target ID:", justify=CENTER).grid(column=1,row=9,sticky=W)
	id_entry = Entry(PanelFrame)
	id_entry.grid(column=2,row=9,sticky=W)
	scale_label = Label(PanelFrame, text="Scaling parameter:", justify=CENTER).grid(column=3,row=9,sticky=W)
	scale_entry = Entry(PanelFrame)
	scale_entry.grid(column=4,row=9,sticky=W)

	#ControlMessage = Label(Panel, text="Click in Canvas before Click in Control Buttons").grid(column=1, row=3, sticky=W)
	#CleanButton = Button(PanelFrame, text="Clean object 1", command=Clean).grid(column=1, row=3, sticky=W)

	mainloop()