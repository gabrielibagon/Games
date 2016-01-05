from Tkinter import *
import random


def mousePressed(event):
	canvas = event.widget.canvas
	redrawAll(canvas)

def keyPressed(event):
	canvas = event.widget.canvas
	if (event.keysym == "Down"):
		moveFallingPiece(canvas, +1, 0)
	elif (event.keysym == "Left"):
		moveFallingPiece(canvas, 0,1)
	elif (event.keysym == "Right"):
		moveFallingPiece(canvas, 0,-1)
	redrawAll(canvas)


def timerFired(canvas):
	ignoreThisTimerEvent = canvas.data["ignoreNextTimerEvent"]
	canvas.data["ignoreNextTimerEvent"] = False
	if ((canvas.data["isGameOver"] == False) and
			(ignoreThisTimerEvent == False)):
			# only process timerFired if game is not over
			drow = canvas.data["tetrisDrow"]
			dcol = canvas.data["tetrisDcol"]
			moveFallingPiece(canvas, drow, dcol)
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

	#for when the game is over
	# if (canvas.data["isGameOver"] == True):
	# 		cx = canvas.data["canvasWidth"]/2
	# 		cy = canvas.data["canvasHeight"]/2
	# 		canvas.create_text(cx, cy, text="Game Over!", fill="white", font=("Helvetica", 32, "bold"))

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

	#this is the pixel of the middle fo the board
	middle = (len(tetrisBoard[0])*cellSize + 5) / 2

	#this is to fill the background of the board (black)
	if (color is None):
		canvas.create_rectangle(left, top, right, bottom, fill="black")
	
	#drawing the tetris piece, one square at a time
	else:
		#drawing non-pink pieces
		locationRow = canvas.data["fallingPieceLocationRow"]
		locationCol = canvas.data["fallingPieceLocationCol"]
		if (color is not "pink"):
			print (color + " PIECE")
			left = (middle - 2*cellSize) + cellSize*col + cellSize*locationRow
			right = (middle - 2*cellSize) + cellSize*(col+1) + cellSize*locationRow
			top = margin + cellSize*row + cellSize*locationCol
			bottom = margin + cellSize*(row+1) + cellSize*locationCol
			# print ("middle", middle)
			# print ("left ",left)
			# print ("right ",right)
			# print ("top ", top)
			# print ("bottom ", bottom) 
			canvas.create_rectangle(left, top, right, bottom, fill= "%s" % color)
		#drawing the pink piece
		else:
			print (color + " PIECE")
			left = (middle - cellSize) + cellSize*col + cellSize*locationRow
			right = (middle - cellSize) + cellSize*(col+1) + cellSize*locationRow
 			top = margin + cellSize*row + cellSize*locationCol
			bottom = margin + cellSize*(row+1) + cellSize*locationRow
			canvas.create_rectangle(left, top, right, bottom, fill= "%s" % color)

def loadTetrisBoard(canvas):
	rows = canvas.data["rows"]
	cols = canvas.data["cols"]
	tetrisBoard = [ ]
	for row in range(rows): tetrisBoard += [[0] *cols] #this sets tetrisBoard to all 0's initially
	# tetrisBoard[rows/2][cols/2] = 1
	canvas.data["tetrisBoard"] = tetrisBoard

def moveFallingPiece(canvas, drow, dcol):
		fallingPieceLocationRow = canvas.data["fallingPieceLocationRow"]
		canvas.data["fallingPieceLocationRow"] = fallingPieceLocationRow - drow
		fallingPieceLocationCol = canvas.data["fallingPieceLocationCol"]
		canvas.data["fallingPieceLocationCol"] = fallingPieceLocationCol - dcol
		drawFallingPiece(canvas)
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
	canvas.data["fallingPieceLocationRow"] = 0
	canvas.data["fallingPieceLocationCol"] = 0
	# row = canvas.data["tetrisDrow"] = 0
	# col = canvas.data["tetrisDcol"] = -1 # start moving left
	# # fallingPieceRow = 0
	# # fallingPieceCol = col/2
	drawFallingPiece(canvas)

def drawFallingPiece(canvas):
	fallingPiece = canvas.data["fallingPiece"]
	fallingPieceColor = canvas.data["fallingPieceColor"]
	tetrisBoard = canvas.data["tetrisBoard"]
	print ("fallingPiece ", fallingPieceColor)
	#clear the piece -> this might need to be specified to the shape of the piece...
	#i'm imagining a bug that causes and issue when other pieces are in this 2x4 buffer
	for row in range(0,2):
		for col in range (0,4):
			print ("this should appear 8 times every click")
			drawTetrisCell(canvas, tetrisBoard,row,col, "black")

	#to keep track of which square of the piece we're drawing
	rowInt = 0
	for row in fallingPiece:
		colInt = 0
		for column in row:
			if (column is True):
				#the function parameters->drawTetrisCell(canvas, tetrisBoard, row, col, color):
				drawTetrisCell(canvas, tetrisBoard,rowInt,colInt, fallingPieceColor)
			colInt += 1
		rowInt += 1


def printInstructions():
	print "Tetris!"
	print "Use the left and right arrow keys to move the piece horizontally."
	print "Eliminate rows"
	print "Don't reach the top!"
	print "Press 'r' to restart."

def init(canvas):
	printInstructions()
	loadTetrisBoard(canvas)

	#red
	iPiece = [
		[True, True, True, True]
	]

	#yellow
	jPiece = [
		[True, False, False],
		[True, True, True]
	]

	#magenta
	lPiece = [
		[False, False, True],
		[True, True, True]
	]

	#pink
	oPiece = [
		[True, True],
		[True, True]
	]

	#cyan
	sPiece = [
		[False, True, True],
		[True, True, False]
	]

	#green
	tPiece = [
		[False, True, False],
		[True, True, True]
	]

	#orange
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