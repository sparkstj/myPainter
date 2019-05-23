from tkinter import *
from tkinter import ttk
import algorithms

canvas_width = 500
canvas_height = 150
brushColor = "#476042"
ObjectId = 0
clickList = []

def drawLine(algorithm):
	global ObjectId # this global goes everywhere
	ObjectId = ObjectId + 1
	try:
		End = clickList.pop()
		Start = clickList.pop()
		algorithms.drawLine(ObjectId, Start, End, algorithm, w)
	except:
		print("Please Select Up to 2 Points in Canvas First. To begin, now select another two points in canvas")
	

def paint( event ):
	x, y = event.x, event.y
	w.create_rectangle(x,y,x,y,fill=brushColor)
	clickList.append((x,y))

master = Tk()
master.title( "Painting board" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.pack(expand = YES, fill = BOTH)
w.bind("<Button-1>", paint)
#w.bind( "<B1-Motion>", paint )
message = Label( master, text = "Click the Buttons" )
message.pack( side = BOTTOM )

Panel = Tk()
Panel.title("This is the Control Panel")
PanelFrame = ttk.Frame(Panel)
PanelFrame.pack()
#PanelFrame.grid(column=0, row=0, sticky=(N, W, E, S))
LineButton1 = Button(PanelFrame, text="Draw Line (DDA)", command= lambda: drawLine("DDA") )
LineButton1.pack( side = LEFT )
LineButton2 = Button(PanelFrame, text="Ready to Draw Line (Bresenham)", command= lambda: drawLine("Bresenham") )
LineButton2.pack( side = RIGHT )
ControlMessage = Label(Panel, text="Click in Canvas before Click in Control Buttons")
ControlMessage.pack ( side = BOTTOM )

mainloop()