from Tkinter import *
import random


def mousePressed(event):
	canvas = event.widget.canvas
	redrawAll(canvas)

def keyPressed(event):
	canvas = event.widget.canvas
	newFallingPiece(canvas)
	redrawAll(canvas)

def timerFired(canvas):
	ignoreThisTimerEvent = canvas.data["ignoreNextTimerEvent"]
	canvas.data["ignoreNextTimerEvent"] = False
	if ((canvas.data["isGameOver"] == False) and
			(ignoreThisTimerEvent == False)):
			# only process timerFired if game is not over
			drow = canvas.data["tetrisDrow"]
			dcol = canvas.data["tetrisDcol"]
			movePiece(canvas, drow, dcol)
			redrawAll(canvas)
	# whether or not game is over, call next timerFired
	# (or we'll never call timerFired again!)
	delay = 150 # milliseconds
	canvas.after(delay, timerFired, canvas) # pause, then call timerFired again

def redrawAll(canvas):
	canvas.delete(ALL)
	drawTetrisBoard(canvas)
	drawFallingPiece(canvas)
	newFallingPiece(canvas)
	if (canvas.data["isGameOver"] == True):
			cx = canvas.data["canvasWidth"]/2
			cy = canvas.data["canvasHeight"]/2
			canvas.create_text(cx, cy, text="Game Over!", fill="white", font=("Helvetica", 32, "bold"))

def drawTetrisBoard(canvas):
	tetrisBoard = canvas.data["tetrisBoard"]
	rows = len(tetrisBoard)
	cols = len(tetrisBoard[0])
	for row in range(rows):
		for col in range(cols):
			drawTetrisCell(canvas, tetrisBoard, row, col, None)

def drawTetrisCell(canvas, tetrisBoard, row, col, color):
	margin = canvas.data["margin"]
	cellSize = canvas.data["cellSize"]
	left = margin + col * cellSize
	right = left + cellSize
	top = margin + row * cellSize
	bottom = top + cellSize
	canvas.create_rectangle(left, top, right, bottom, fill="black")
	if (color is not None):
		# draw part of the tetris body
		print left
		print top
		print right
		print bottom
		canvas.create_rectangle(left, top, right, bottom, fill= "%s" % color)
	elif (tetrisBoard[row][col] < 0):
		# draw food
		canvas.create_rectangle(left, top, right, bottom, fill="green")
	# for debugging, draw the number in the cell


def loadTetrisBoard(canvas):
	rows = canvas.data["rows"]
	cols = canvas.data["cols"]
	tetrisBoard = [ ]
	for row in range(rows): tetrisBoard += [[0] *cols] #this sets tetrisBoard to all 0's initially
	# tetrisBoard[rows/2][cols/2] = 1
	canvas.data["tetrisBoard"] = tetrisBoard

def movePiece(canvas, drow, dcol):
		canvas.data["pieceDrow"] = drow # store direction for next timer event
		canvas.data["pieceDcol"] = dcol
		tetrisBoard = canvas.data["tetrisBoard"]
		rows = len(tetrisBoard)
		cols = len(tetrisBoard[0])
		# headRow = canvas.data["headRow"]
		# headCol = canvas.data["headCol"]
		# newHeadRow = headRow + drow
		# newHeadCol = headCol + dcol
		# tetrisBoard[newHeadRow][newHeadCol] = 1 + tetrisBoard[headRow][headCol];
		# canvas.data["headRow"] = newHeadRow
		# canvas.data["headCol"] = newHeadCol
		# removeTail(canvas)

def newFallingPiece(canvas):
	pieceNumber = random.randrange(0,7)
	canvas.data["fallingPiece"] = canvas.data["tetrisPieces"][pieceNumber]
	canvas.data["fallingPieceColor"] = canvas.data["tetrisPieceColors"][pieceNumber]
	# row = canvas.data["tetrisDrow"] = 0
	# col = canvas.data["tetrisDcol"] = -1 # start moving left
	# # fallingPieceRow = 0
	# # fallingPieceCol = col/2
	drawFallingPiece(canvas)

def drawFallingPiece(canvas):
	fallingPiece = canvas.data["fallingPiece"]
	fallingPieceColor = canvas.data["fallingPieceColor"]
	tetrisBoard = canvas.data["tetrisBoard"]
	for row in fallingPiece:
		rowInt = 0
		for column in row:
			if True:
				drawTetrisCell(canvas, tetrisBoard,rowInt,column, fallingPieceColor)
		rowInt = rowInt+1


def printInstructions():
	print "Tetris!"
	print "Use the left and right arrow keys to move the piece horizontally."
	print "Eliminate rows"
	print "Don't reach the top!"
	print "Press 'r' to restart."

def init(canvas):
	printInstructions()
	loadTetrisBoard(canvas)

	iPiece = [
		[True, True, True, True]
	]

	jPiece = [
		[True, False, False ],
		[True, True, True]
	]

	lPiece = [
		[False, False, True],
		[True, True, True]
	]

	oPiece = [
		[True, True],
		[True, True]
	]

	sPiece = [
		[False, True, True],
		[True, True, False]
	]

	tPiece = [
		[False, True, False],
		[True, True, True]
	]

	zPiece = [
		[True, True, False],
		[False, True, True]
	]

	tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
	tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
	canvas.data["tetrisPieces"] = tetrisPieces
	canvas.data["tetrisPieceColors"] = tetrisPieceColors
	canvas.data["isGameOver"] = False
	canvas.data["ignoreNextTimerEvent"] = False
	canvas.data["tetrisDrow"] = 0
	canvas.data["tetrisDcol"] = -1 # start moving left
	pieceNumber = random.randrange(0,7)
	canvas.data["fallingPiece"] = tetrisPieces[pieceNumber]
	canvas.data["fallingPieceColor"] = tetrisPieceColors[pieceNumber]
	# canvas.data["fallingPieceColor"] =

def run():
	root = Tk()
	rows = 30
	cols = 15
	cellSize = 25
	margin = 5
	canvasWidth = 2*margin + cols*cellSize
	canvasHeight = 2*margin + rows*cellSize
	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.pack()
	root.resizable(width=0, height=0)
	root.canvas = canvas.canvas = canvas
	canvas.data = { }
	canvas.data["margin"] = margin
	canvas.data["cellSize"] = cellSize
	canvas.data["canvasWidth"] = canvasWidth
	canvas.data["canvasHeight"] = canvasHeight
	canvas.data["rows"] = rows
	canvas.data["cols"] = cols
	init(canvas)


	root.bind("<Button-1>", mousePressed)
	root.bind("<Key>", keyPressed)
	# timerFired(canvas)
	# and launch the app
	root.mainloop()

run()