from tkinter import *
from tkinter import ttk
import algorithms
from Objects import Objects
from PIL import Image, ImageDraw

canvas_width = 500
canvas_height = 150
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
	Objects.xyList.append([])
	print(Objects.ObjectId)
	drawLine = True
	clickList.clear()
	
def PolygonSignal():
	global drawPolygon
	drawPolygon = True
	Objects.ObjectId = Objects.ObjectId + 1
	Objects.obList.append([])
	Objects.xyList.append([])
	#print(ObjectId)
	clickList.clear()

def EllipseSignal():
	try:
		Objects.ObjectId = Objects.ObjectId + 1
		Objects.obList.append([])
		Objects.xyList.append([])
		leftup = MotionList[0]
		rightdown = MotionList[len(MotionList)-1]
		center = (int((leftup[0]+rightdown[0])/2), int((leftup[1]+rightdown[1])/2))
		longradius = int(abs(leftup[0]-rightdown[0])/2)
		shortradius = int(abs(leftup[1]-rightdown[1])/2)
		algorithms.drawEllipse(Objects.ObjectId, center, (longradius, shortradius), w, algorithm.get(), Objects.brushColor)
		MotionList.clear()
	except:
		Objects.ObjectId = Objects.ObjectId - 1
		print("please select the ellipse district first")
		
def CurveSignal():
	global drawCurve
	Objects.ObjectId = Objects.ObjectId + 1
	Objects.obList.append([])
	Objects.xyList.append([])
	drawCurve = True
	#print(Objects.ObjectId)
	if (len(clickList)>=2): #Curve Control Points should be selected before clicking the button
		print("Curve {} with control points {} using Algorithm {}".format(Objects.ObjectId,clickList,algorithm.get()))
		algorithms.drawCurve(Objects.ObjectId, clickList.copy(), algorithm.get(), w, Objects.brushColor)
		clickList.clear()
		drawCurve = False
	clickList.clear()

def TranslateSignal(id):
	id = int(id)
	p1 = MotionList[0]
	p2 = MotionList[len(MotionList)-1]
	MotionList.clear()
	algorithms.translate(id,(p2[0]-p1[0],p2[1]-p1[1]),w)

def RotateSignal(id, r): #must select points before rotate
	id = int(id)
	r = float(r)
	center = clickList.pop()
	algorithms.rotate(id, center, r, w)

def ScaleSignal(id, s):
	id = int(id)
	s = float(s)
	center = clickList.pop()
	algorithms.scale(id, center, s, w)

def drag( event):
	MotionList.append((event.x, event.y))
	
def paint( event ):
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
	


master = Tk()
master.title( "Painting board" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.width,w.height = canvas_width, canvas_height
w.pack(expand = YES, fill = BOTH)
w.bind("<Button-1>", paint)
w.bind( "<B1-Motion>", drag )
message = Label( master, text = "Click the Buttons" )
message.pack( side = BOTTOM )

Panel = Tk()
Panel.columnconfigure(0, weight=1)
Panel.rowconfigure(0, weight=1)
PanelFrame = ttk.Frame(Panel, padding="4 4 12 12")
PanelFrame.grid(column=0, row=0, sticky=(N, W, E, S))
Panel.title("This is the Control Panel")

algorithm_label = Label(PanelFrame, text='Algorithm:').grid(column=4,row=1,sticky=W)
algorithm = StringVar(Panel)
option = ["DDA","Bresenham","MidPointCircle","Bezier","B-spline"]
algorithm.set(option[0])
#print(algorithm.get())
algorithm_om = OptionMenu(PanelFrame, algorithm, *option)
algorithm_om.grid(column=5,row=1,sticky=W)

LineButton1 = Button(PanelFrame, text="Draw Line", command= LineSignal ).grid(column=1, row=1, sticky=W)
PolygonButton = Button(PanelFrame, text="Draw Polygon", command=PolygonSignal).grid(column=1, row=2, sticky=W)
EllipseButton = Button(PanelFrame, text="Draw Ellipse", command=EllipseSignal).grid(column=1, row=3, sticky=W)
CurveButton = Button(PanelFrame, text="Draw Curve", command=CurveSignal).grid(column=1, row=4, sticky=W)
name_label = Label(PanelFrame, text="name:").grid(column=2, row=5, sticky=W)
name_entry = Entry(PanelFrame)
name_entry.grid(column=3,row=5,sticky=W)
name_entry.focus_set()
name_button = Button(PanelFrame, text="Save Canvas", command = lambda: algorithms.saveCanvas(name_entry, w)).grid(column=1,row=5,sticky=W)
width_label = Label(PanelFrame, text="width:").grid(column=2, row=6, sticky=W)
width_entry = Entry(PanelFrame)
width_entry.grid(column=3,row=6,sticky=W)
height_label = Label(PanelFrame, text="height:").grid(column=4, row=6, sticky=W)
height_entry = Entry(PanelFrame)
height_entry.grid(column=5,row=6,sticky=W)
width_button = Button(PanelFrame, text='Reset Canvas', command = lambda: algorithms.resetCanvas(width_entry,height_entry,w)).grid(column=1,row=6,sticky=W)
r_label = Label(PanelFrame, text="R:", justify=CENTER).grid(column=2,row=7,sticky=W)
r_entry = Entry(PanelFrame)
r_entry.grid(column=3,row=7,sticky=W)
g_label = Label(PanelFrame, text="G:", justify=CENTER).grid(column=4,row=7,sticky=W)
g_entry = Entry(PanelFrame)
g_entry.grid(column=5,row=7,sticky=W)
b_label = Label(PanelFrame, text="B:").grid(column=6,row=7,sticky=W)
b_entry = Entry(PanelFrame)
b_entry.grid(column=7,row=7,sticky=W)
rgb_button = Button(PanelFrame, text="Set Color", command= lambda: algorithms.setColor(r_entry,g_entry,b_entry,w)).grid(column=1,row=7,sticky=W)
translate_label = Label(PanelFrame, text="Target ID:", justify=CENTER).grid(column=2,row=8,sticky=W)
translate_entry = Entry(PanelFrame)
translate_entry.grid(column=3,row=8,sticky=W)
translate_button = Button(PanelFrame, text="Translate", command=lambda: TranslateSignal(translate_entry.get())).grid(column=1,row=8,sticky=W)
rotate_label = Label(PanelFrame, text="Target ID:", justify=CENTER).grid(column=2,row=9,sticky=W)
rotate_entry = Entry(PanelFrame)
rotate_entry.grid(column=3,row=9,sticky=W)
angle_label = Label(PanelFrame, text="Rotation angle:", justify=CENTER).grid(column=4,row=9,sticky=W)
angle_entry = Entry(PanelFrame)
angle_entry.grid(column=5,row=9,sticky=W)
rotate_button = Button(PanelFrame, text="Rotate", command=lambda: RotateSignal(rotate_entry.get(), angle_entry.get())).grid(column=1,row=9,sticky=W)
sid_label = Label(PanelFrame, text="Target ID:", justify=CENTER).grid(column=2,row=10,sticky=W)
sid_entry = Entry(PanelFrame)
sid_entry.grid(column=3,row=10,sticky=W)
scale_label = Label(PanelFrame, text="Scaling parameter:", justify=CENTER).grid(column=4,row=10,sticky=W)
scale_entry = Entry(PanelFrame)
scale_entry.grid(column=5,row=10,sticky=W)
scale_button = Button(PanelFrame, text="Scale", command=lambda: ScaleSignal(sid_entry.get(), scale_entry.get())).grid(column=1,row=10,sticky=W)

#ControlMessage = Label(Panel, text="Click in Canvas before Click in Control Buttons").grid(column=1, row=3, sticky=W)
#CleanButton = Button(PanelFrame, text="Clean object 1", command=Clean).grid(column=1, row=3, sticky=W)

mainloop()