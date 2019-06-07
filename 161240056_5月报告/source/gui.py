from tkinter import *
from tkinter import ttk
import algorithms
from Objects import Objects

canvas_width = 500
canvas_height = 150
brushColor = "#476042"
ObjectId = -1
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
	global ObjectId
	ObjectId = ObjectId + 1
	Objects.obList.append([])
	#print(ObjectId)
	drawLine = True
	clickList.clear()
	
def PolygonSignal():
	global drawPolygon
	global ObjectId
	drawPolygon = True
	ObjectId = ObjectId + 1
	Objects.obList.append([])
	#print(ObjectId)
	clickList.clear()

def EllipseSignal():
	try:
		global ObjectId
		ObjectId = ObjectId + 1
		Objects.obList.append([])
		leftup = MotionList[0]
		rightdown = MotionList[len(MotionList)-1]
		center = (int((leftup[0]+rightdown[0])/2), int((leftup[1]+rightdown[1])/2))
		longradius = int(abs(leftup[0]-rightdown[0])/2)
		shortradius = int(abs(leftup[1]-rightdown[1])/2)
		algorithms.drawEllipse(ObjectId, center, (longradius, shortradius), w, algorithm.get())
		MotionList.clear()
	except:
		ObjectId = ObjectId - 1
		print("please select the ellipse district first")
		
def CurveSignal():
	global drawCurve
	global ObjectId
	ObjectId = ObjectId + 1
	Objects.obList.append([])
	drawCurve = True
	#print(ObjectId)
	if (len(clickList)>=2): #Curve Control Points should be selected before clicking the button
		print("Curve {} with control points {} using Algorithm {}".format(ObjectId,clickList,algorithm.get()))
		algorithms.drawCurve(ObjectId, clickList.copy(), algorithm.get(), w)
		clickList.clear()
		drawCurve = False
	clickList.clear()


def drag( event):
	MotionList.append((event.x, event.y))
	
def paint( event ):
	global drawLine
	global drawPolygon
	global drawCurve
	x, y = event.x, event.y
	variable = w.create_rectangle(x,y,x,y,fill=brushColor)
	#print(drawCurve)
	if (drawLine == True) or (drawPolygon == True):
		Objects.obList[ObjectId].append(variable)
	clickList.append((x,y))
	if (drawLine == True )and(len(clickList)>=2):
		End = clickList.pop()
		Start = clickList.pop()
		clickList.clear()
		algorithms.drawLine(ObjectId, Start, End, algorithm.get(), w)
		print("Line {} from {} to {}, using Algorithm {}".format(ObjectId, Start, End, algorithm.get()))
		drawLine = False
	if (drawPolygon == True) and (len(clickList)>=2):
		if (Manhattan(clickList[0], (x,y)) < 8): 
			print("Polygon {} using Algorithm {}".format(ObjectId,algorithm.get()))
			algorithms.drawLine(ObjectId, clickList[len(clickList)-2],clickList[0], algorithm.get(), w )
			clickList.clear()
			#drawPolygon = False
			#Objects.obList.append([])
			drawPolygon = False
		else:
			algorithms.drawLine(ObjectId, clickList[len(clickList)-2],clickList[len(clickList)-1], algorithm.get(), w )



		
def Clean():
	print("clean")
	for i in Objects.obList[1]:
		w.delete(i)
	Objects.obList.pop(1)
	#for j in Objects.obList:
	#	for i in j:
	#		algorithms.drawPixel(i[0],i[1],w,-1,brushColor)
	


master = Tk()
master.title( "Painting board" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
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
print(algorithm.get())
algorithm_om = OptionMenu(PanelFrame, algorithm, *option)
algorithm_om.grid(column=5,row=1,sticky=W)

LineButton1 = Button(PanelFrame, text="Draw Line", command= LineSignal ).grid(column=1, row=1, sticky=W)
PolygonButton = Button(PanelFrame, text="Draw Polygon", command=PolygonSignal).grid(column=1, row=2, sticky=W)
EllipseButton = Button(PanelFrame, text="Draw Ellipse", command=EllipseSignal).grid(column=1, row=3, sticky=W)
CurveButton = Button(PanelFrame, text="Draw Curve", command=CurveSignal).grid(column=1, row=4, sticky=W)
#ControlMessage = Label(Panel, text="Click in Canvas before Click in Control Buttons").grid(column=1, row=3, sticky=W)
#CleanButton = Button(PanelFrame, text="Clean object 1", command=Clean).grid(column=1, row=3, sticky=W)

mainloop()