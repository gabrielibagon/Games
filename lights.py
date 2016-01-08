from Tkinter import *
import random


def mousePressed(event):
	canvas = event.widget.canvas

def keyPressed(event):
	canvas = event.widget.canvas
	if (event.char == "q"):
		close_window(canvas)
	if (event.char == " "):	
		changePattern(canvas)

def close_window(canvas):
	root = canvas.data["root"]
	root.destroy()

def timerFired(canvas):
	drawTetrisBoard(canvas)
	delay = 1 # milliseconds
	canvas.after(delay, timerFired, canvas) # pause, then call timerFired again

def loadTetrisBoard(canvas):
	rows = canvas.data["rows"]
	cols = canvas.data["cols"]
	tetrisBoard = [ ]
	for row in range(rows): tetrisBoard += [[0] *cols] #this sets tetrisBoard to all 0's initially
	# tetrisBoard[rows/2][cols/2] = 1
	canvas.data["tetrisBoard"] = tetrisBoard

def drawTetrisBoard(canvas):
	for row in range(canvas.data["rows"]):
		for col in range(canvas.data["cols"]):
			de=("%02x"%random.randint(0,255))
			re=("%02x"%random.randint(0,255))
			we=("%02x"%random.randint(0,255))
			ge="#"
			color=ge+de+re+we
			drawTetrisCell(canvas, row, col, color)

def drawTetrisCell(canvas, row, col, color):
	margin = canvas.data["margin"]
	cellSize = canvas.data["cellSize"]
	left = margin + col * cellSize
	right = left + cellSize
	top = margin + row * cellSize
	bottom = top + cellSize
	canvas.create_rectangle(left, top, right, bottom, fill=color)

def init(canvas):
	loadTetrisBoard(canvas)

def run():
	root = Tk()
	rows = 25
	cols = 25
	cellSize = 10
	margin = 0
	canvasWidth = 2*margin + cols*cellSize
	canvasHeight = 2*margin + rows*cellSize
	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.pack()
	root.resizable(width=0, height=0)
	root.attributes('-fullscreen', True)
	root.canvas = canvas.canvas = canvas
	canvas.data = { }
	canvas.data["root"] = root
	canvas.data["margin"] = margin
	canvas.data["cellSize"] = cellSize
	canvas.data["canvasWidth"] = canvasWidth
	canvas.data["canvasHeight"] = canvasHeight
	canvas.data["rows"] = rows
	canvas.data["cols"] = cols
	init(canvas)
	root.bind("<Button-1>", mousePressed)
	root.bind("<Key>", keyPressed)
	timerFired(canvas)
	# and launch the app
	root.mainloop()

run()