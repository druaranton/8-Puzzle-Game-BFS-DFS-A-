#Aranton, Andreau O.
#2020-00947
#09/19/2022
#CMSC 170 EXER 3

#import tkinter for the GUI
from tkinter import *
#for the dialog
from tkinter.filedialog import askopenfilename
import time

#puzzleNode class
class PuzzleNode:
	#the object contains the puzzle, the index/location of the 0, the action, and its parent object
	 def __init__(self, puzzle, empty_loc, action, parent):
	 	self.puzzle = puzzle
	 	self.empty_loc = empty_loc
	 	self.action = action
	 	self.parent = parent

#APuzzleNode class that would be used for the A* search. It is a subclass of the PuzzleNode class
class APuzzleNode(PuzzleNode):
	def __init__(self, puzzle, empty_loc, action, parent, f, g, h):
		super().__init__(puzzle, empty_loc, action, parent)
		self.f = f
		self.g = g
		self.h = h

#function to compute the H
def computeH(puzzle):
	valueH = 0 #initial value of H
	goalPuzzle = [[1,2,3],[4,5,6],[7,8,0]] #the puzzle goal
	for i in range(0, 9): #for every number in the puzzle
		if i == 0: #if i is zero, proceed to next iteration
			continue
		for j, k in enumerate(puzzle): #j is the index and k is the the jth element of the puzzle(also a list)
			try:
				curLocation = [j, k.index(i)] #list with the first element as the j and the second element is the index of i in k
				break
			except: #if i is not in k, pass
				pass

		for l, m in enumerate(goalPuzzle):
			try:
				goalLocation = [l, m.index(i)] #j is the index and k is the the jth element of the puzzle(also a list)
				break
			except: #if i is not in k, pass
				pass

		valueH +=  abs(curLocation[0] - goalLocation[0]) #add the absolute difference of the rows to the valueH
		valueH +=  abs(curLocation[1] - goalLocation[1]) #add the absolute difference of the columns to the valueH
	return valueH #return valueH

#function to write the steps into a file
def writeSolution(solution):
	filehandle = open("puzzle.out", "w") #open the file
	for i in solution:
		filehandle.write(i + " ") #write the actions
	filehandle.close() #close the file

#BFS
def BFSearch():
	start = time.time()
	initial = PuzzleNode(multiArray, [rowZero, colZero], None, None) #creates a PuzzleNode
	frontier = [initial]
	explored = []
	while len(frontier) != 0: #while frontier is not empty
		print(len(explored))
		currentState = frontier.pop(0) #dequeue
		explored.append(currentState) #append the explored list
		if goalTest(getOneDimenArray(currentState.puzzle)): #if the puzzle is the goal
			end = time.time()
			print(end - start)
			traceSolution(currentState) #trace the solution
			return currentState
		else:
			excludeList = frontier + explored #frontier and explored is not included
			for action in actions(currentState): #for all the possible actions
				possiblePuzzle, zeroPos = result(currentState, action) #creates the puzzle based on action and its zero location
				if possiblePuzzle not in [puz.puzzle for puz in excludeList]: #if the puzzle is not in exluded list
					frontier.append(PuzzleNode(possiblePuzzle, zeroPos, action, currentState)) #enque a node of the puzzle

#DFS 
def DFSearch():
	start = time.time()
	initial = PuzzleNode(multiArray, [rowZero, colZero], None, None) #creates a puzzleNode
	frontier = [initial]
	explored = []
	while len(frontier) != 0: #while frontier is not empty
		print(len(explored))
		currentState = frontier.pop() #pop the top stack
		explored.append(currentState) #insert the top stack in the explored
		if goalTest(getOneDimenArray(currentState.puzzle)): #if the goal is 
			end = time.time()
			print(end - start)
			traceSolution(currentState) #trace the solution
			return currentState
		else:
			excludeList = frontier + explored #frontier and explored is not included
			for action in actions(currentState): #for all the possible actions
				possiblePuzzle, zeroPos = result(currentState, action) #creates the puzzle based on action and its zero location
				if possiblePuzzle not in [puz.puzzle for puz in excludeList]: #if the puzzle is not in exluded list
					frontier.append(PuzzleNode(possiblePuzzle, zeroPos, action, currentState)) #enque a node of the puzzle

#A* Search
def aStarSearch():
	start = time.time()
	initial = APuzzleNode(multiArray, [rowZero, colZero], None, None, computeH(multiArray), 0, computeH(multiArray)) #creates a APuzzleNode object
	openList = [initial] #the intital is added to the openList
	closedList = [] #closedlist or explored list
	while len(openList) != 0: #while openList is not empty
		print(len(closedList))
		bestNode = removeMinF(openList) #the best node will be fetched using the removeMinF()
		closedList.append(bestNode) #add the best node to the closedList
		if goalTest(getOneDimenArray(bestNode.puzzle)): #if the bestnode puzzle is the goal puzzle
			end = time.time()
			print(end - start)
			traceSolution(bestNode) #trace the solution
			return bestNode

		excludeList = openList + closedList #openlist and closed list is on 
		for action in actions(bestNode): #for every available action
			possiblePuzzle, zeroPos = result(bestNode, action) #creates the puzzle based on action and its zero location
			
			possibleG = bestNode.g + 1 #the g is the best node's g + 1
			possibleH = computeH(possiblePuzzle) #compute the H
			possibleF = possibleG + possibleH #F = G+H
			canAdd = False #flag to know whether the node can be added to the openList
			if possiblePuzzle in [puz.puzzle for puz in openList]: #if the possible puzzle is in the openlist
				for i in openList: #for every element of the openList
					if i.puzzle == possiblePuzzle: #if the puzzle is equal to the possible puzzle
						if possibleG < i.g: #if the possible puzzle's G is less than the G of the puzzle in openList
							canAdd = True #canAdd would be true
							break #break the loop
						# else:
						# 	canAdd = False
			if (possiblePuzzle not in [puz.puzzle for puz in excludeList]) or canAdd == True: #if possible puzzle is not in excludeList or if the the flag is true
				openList.append(APuzzleNode(possiblePuzzle, zeroPos, action, bestNode, possibleF, possibleG, possibleH)) #add the node/puzzle in the openList

#function to remove the node with minimum F from the list and return it
def removeMinF(openList):
	toRemove = min(openList, key=lambda i: i.f) #min() function where the key is i.f (the comparison is the f value)
	openList.remove(toRemove) #remove the node from the openList
	return toRemove #return the node


#function to make a copy of the puzzle
def copyPuzzle(puz):
	cPuzzle = [[0 for i in range(3)] for j in range(3)] #creates a 2d array like the puzzle full of 0s
	#copies the puzzle
	for i in range(3):
		for j in range(3):
			cPuzzle[i][j] = puz[i][j]
	return cPuzzle

#function to trace the solution
def traceSolution(currentState):
	global boardSol
	solution = [] #list to put the actions
	while currentState.parent != None: #while the parent is not none
		solution.append(currentState.action) #append the solution list with action
		currentState = currentState.parent #update the current state
	solution.reverse() #reverse the list to have the right solution
	writeSolution(solution) #write it in a file
	boardSol = solution #update the boardSol global variable

#function to get the path cost
def pathCost(solution):
	return len(solution) #the path cost is the number of swaps/actions made to make it to the goal



#result function which returns the resulting puzzle based on action and its zero location					
def result(currentState, action):
	row = currentState.empty_loc[0]
	col = currentState.empty_loc[1]
	curState = copyPuzzle(currentState.puzzle)
	#print(curState)
	if action == "U": #if action is UP
		curState[row][col] = curState[row-1][col]
		curState[row-1][col] = 0
		return curState, [row-1,col]
	elif action == "R": #if action is Right
		curState[row][col] = curState[row][col+1]
		curState[row][col+1] = 0
		return curState, [row,col+1]
	elif action == "D": #if action is Down
		curState[row][col] = curState[row+1][col]
		curState[row+1][col] = 0
		#print(curState)
		#print(row)
		return curState, [row+1,col]
	elif action == "L": #if action is Left
		curState[row][col] = curState[row][col-1]
		curState[row][col-1] = 0
		return curState, [row,col-1]
	return None

#function that returns the valid or possible actions that can be done in the puzzle
def actions(curState):
	viableActions = [] #list to store all the possible actions
	#If the 0 is not in the top
	if curState.empty_loc[0] != 0:
		viableActions.append("U")
	#If 0 is not in the right
	if curState.empty_loc[1] != 2:
		viableActions.append("R")
	#If 0 is not in the bottom
	if curState.empty_loc[0] != 2:
		viableActions.append("D")
	#If 0 is not in the left
	if curState.empty_loc[1] != 0:
		viableActions.append("L")
	return viableActions

#render tiles function
def renderTiles():
	global rowZero, colZero
	tiles = [[0]*3 for i in range(3)] #creates a multidimentional list 3x3 (like a matrix)
	#nested loop for the creation of grids
	for j in range(0,3):
		for k in range(0,3):
			if multiArray[j][k] == 0: #if the number is zero
				rowZero = j
				colZero = k
				tiles[j][k] = Label(frame2, text= "", width=10, height=5,bg="#B3A580", borderwidth=2, relief="solid", font=("Arial", 15)) #the generated label's text would be blank
			else: #if the number is not zero
				tiles[j][k] = Label(frame2, text= str(multiArray[j][k]), width=10, height=5, bg="#B3A580", borderwidth=2, relief="solid", font=("Arial", 15)) #generates the label with the number as the text
			tiles[j][k].grid(row=j, column=k) #the label's would be arranged like a grid
			if inGame == True: #if it is still in-game, the tile would be clickable wherein move function will execute whenever clicked.
				tiles[j][k].bind("<Button>", move)
			else: #if the game is over, the color of the tiles would be orange
				tiles[j][k].config(bg="#685642")

#function to load the puzzle from a file into a list of list
def loadPuzzle():
	global multiArray
	multiArray = []
	filehandle = open(fileToOpen, "r") #open the file as read-only
	if filehandle is not None:
		for line in filehandle: #for every line
			line = line.rstrip('\n').split(" ") #remove the extra new line if there's any and then split them
			intLine = [int(x) for x in line] #since the line is a list of strings, convert them into a list of int
			multiArray.append(intLine) #append/place them in the multiArray
	filehandle.close()

#function to load a file
def loadFile():
	global fileToOpen
	fileToOpen = askopenfilename(parent=root) #makes the user select a file
	if fileToOpen != '': #if the user selected a file
		loadPuzzle() #load the puzzle
		reset() #reset
	else:
		fileToOpen = 'puzzle.in' #default value

#reset funtion
def reset():
	renderTiles() #render the tiles
	statusArea.config(text= status()) #update the status bar


#function to check the sides if it is near the 0/blank tile
def checkSides(array, row, col):
	if row < 0 or col < 0: #if the colunn or row is 0
		return False
		#the row or col could be negative so a try-except is used
	try:
		return array[row][col] == 0
	except:
		return False

#function to get the one dimensional list of the list of lists
def getOneDimenArray(array):
	monoList = [] #this is where the elements would be placed
	for i in array: #for every element of the multidimensional array
		monoList.extend(i) #extend the monoList
	return monoList #return monoList
	
#function to check if the user won
def goalTest(puzzle):
	winList = list(range(1,9)) #create's a list where the elements are from 1 to 9
	winList.append(0) #appends the list so that the list would be the winning list
	if puzzle == winList: #if the multiList's flat list equivalent is equal to the winning list
		return True
	else:
		return False

#function to check if the puzzle is solvable
def isSolveable():
	monoList = getOneDimenArray(multiArray) #get the flat list equivalent of the multilist
	invCounter = 0 #inversions counter
	#nested loop to get the inversion/s
	for i in range(0, 9):
		for j in range(i+1, 9):
			if monoList[i] > 0 and monoList[j] > 0 and monoList[i] > monoList[j]: #if it is not the first tile and if the value of the current tile is greater than the next tile
				invCounter += 1 #increments the counter by 1
	return invCounter % 2 == 0 #returns true if the number of inversions is even. otherwise, false

#function to move the tiles
def move(event):
	global inGame #so that the global variable inGame's value can get updated
	row = event.widget.grid_info()["row"] #gets the row number to the clicked tile
	col = event.widget.grid_info()["column"]  #gets the column number of the clicked tile
	text = event.widget.cget("text") #gets the text of the clicked tile
	if text != "": #if the clicked tile is not the empty tile
		if checkSides(multiArray, row - 1, col): #if the tile above is empty
			#swaps the value of the tile
			multiArray[row - 1][col] = int(text) 
			multiArray[row][col] = 0
			if goalTest(getOneDimenArray(multiArray)): #check if the user wins
				inGame = False #the game is over
				statusArea.config(text="YOU WON!") #updates the status bar/area's text
			renderTiles() #reflect the changes
		elif checkSides(multiArray, row + 1, col): #else if the tile below is empty
			#swaps the value of the tile
			multiArray[row + 1][col] = int(text)
			multiArray[row][col] = 0
			if goalTest(getOneDimenArray(multiArray)): #check if the user wins
				inGame = False #the game is over
				statusArea.config(text="YOU WON!") #updates the status bar/area's text
			renderTiles() #reflect the changes
		elif checkSides(multiArray, row, col -1): #else if the tile on the left is empty
			#swaps the value of the tile
			multiArray[row][col -1] = int(text)
			multiArray[row][col] = 0
			if goalTest(getOneDimenArray(multiArray)): #check if the user wins
				inGame = False #the game is over
				statusArea.config(text="YOU WON!") #updates the status bar/area's text
			renderTiles() #reflect the changes
		elif checkSides(multiArray, row, col +1): #else if the tile on the rigth is empty
			#swaps the value of the tile
			multiArray[row][col +1] = int(text)
			multiArray[row][col] = 0
			if goalTest(getOneDimenArray(multiArray)): #check if the user wins
				inGame = False #the game is over
				statusArea.config(text="YOU WON!") #updates the status bar/area's text
			renderTiles() #reflect the changes

#function to get the status whether the puzzle is solvable or not
def status():
	if isSolveable(): #if it is solvable
		return "Solvable. You can do this!"
	else: #if it is not
		return "Non-solvable"

#function that calls the dfs or bfs method, when solve button is clicked
def solve():
	global inGame
	global indexSol
	indexSol = 0 #resets the indexSol
	loadPuzzle() #reloads the puzzle
	inGame = False #updates the inGame
	renderTiles() #renders the tiles
	currentMethod = clicked.get() #check the option selected by user
	if currentMethod == "BFS":
		BFSearch()
	elif currentMethod == "DFS":
		DFSearch()
	else:
		aStarSearch()
	solveButton.configure(text="Next", command = nextClick) #updates the button
	solLabel.config(text= boardSol) #show the solution/actions
	fileButton.config(state="disabled") #deactivate the select file

#function to execute when next button is clicked
def nextClick():
	global indexSol
	global multiArray
	lenSolution = pathCost(boardSol) #gets the cost
	if boardSol[indexSol] == "U": #if the action is up
		multiArray[rowZero][colZero] = multiArray[rowZero-1][colZero]
		multiArray[rowZero -1][colZero] = 0
		renderTiles()
	elif boardSol[indexSol] == "R": #if the action is right
		multiArray[rowZero][colZero] = multiArray[rowZero][colZero+1]
		multiArray[rowZero][colZero+1] = 0
		renderTiles()
	if boardSol[indexSol] == "D": #if the action is down
		multiArray[rowZero][colZero] = multiArray[rowZero+1][colZero]
		multiArray[rowZero+1][colZero] = 0
		renderTiles()
	elif boardSol[indexSol] == "L": #if the action is left
		multiArray[rowZero][colZero] = multiArray[rowZero][colZero-1]
		multiArray[rowZero][colZero-1] = 0
		renderTiles()
	indexSol+= 1 #increments the indexSol
	if indexSol == lenSolution: #if the solution is done
		statusArea.config(text="YOU WON!") #updates the status bar/area's text
		solveButton.config(state="disabled") #disables the button
		showCost(lenSolution) #show the cost

#funtion to show the cost in another window
def showCost(cost):
	costWindow = Toplevel(root) #intstantiate new window
	costWindow.title("Solution Cost") #title of window
	costWindow.geometry("300x200") #size 0f window
	Label(costWindow, text = "Path cost: " + str(cost), font=("Arial", 15)).pack(expand=True) #label that show the cost
	Button(costWindow, text="OK", command = costWindow.destroy).pack(expand=True)

#function that will update the button once a choice from dropdown is clicked
def updateSolveButton(clicked):
	solveButton.config(text="SOLUTION", command = solve, state="normal") #updates the button

fileToOpen = 'puzzle.in'
rowZero = 0
colZero = 0
indexSol = 0
boardSol = []
inGame = True #the game is initialy inGame
multiArray = [] #array where the array of elemets(puzzle) would get stored
loadPuzzle() #loads the puzzle
#aStarSearch()
root = Tk() #initialize tkinter
root.title("8 Puzzle") #sets the window title
#print(root.winfo_width())
# root.geometry("400x500")
root.resizable(0,0) #disables the maximize button
frame0 = Frame(root, bg="#F4F0CB")
frame0.pack(side=TOP, fill=X) #the f#F4F0CBrame is of pack, will fill horizontally
frame1 = Frame(root, bg="#F4F0CB") #frame for the status area
frame1.pack(side=TOP, fill=X) #the f#F4F0CBrame is of pack, will fill horizontally
frame2 = Frame(root) #frame2 is for the grid
frame2.pack(side=TOP, fill=X) #pack as well, will fill horizontally
frame3 = Frame(root, bg="#F4F0CB") #frame for the actions
frame3.pack(side=TOP, fill=X)
frame4 = Frame(root, bg="#F4F0CB") #frame for the buttons
frame4.pack(side=TOP, fill=X)

fileButton = Button(frame0, text="Select file..", command = lambda:loadFile())
fileButton.pack()
statusArea = Label(frame1, text= status(), height=3,font=("Minecraft", 15), bg="#F4F0CB") #creates a label widget for the status area
statusArea.pack() #it is a pack
clicked = StringVar()
clicked.set("BFS")
options = ["BFS", "DFS", "A* Search"] #for the dropdown menu
dropdown = OptionMenu(frame4, clicked, *options, command = updateSolveButton) #dropdown menu
dropdown.pack(side=LEFT, expand =0.5) #to make it in middle
solLabel = Label(frame3, text="", font=("Arial", 15), fg="gray", bg="#F4F0CB", wraplength=300) #label for the solution action
solLabel.pack()
solveButton = Button(frame4, text="SOLUTION", command = solve) #button for solving
solveButton.pack(side=LEFT, expand=0.5) #middle
if not isSolveable(): #if the puzzle is unsolvable
	solveButton.config(state="disabled") #disable the button
renderTiles() #render the tiles
root.mainloop() #mainloop


#resources/links used
#https://www.youtube.com/watch?v=YXPyB4XeYLA&t=1742s
#https://stackoverflow.com/questions/58898696/how-to-get-the-row-and-column-number-for-a-widget-placed-in-grid-in-tkinter-pyth
#https://stackoverflow.com/questions/17267140/python-pack-and-grid-methods-together
#https://stackoverflow.com/questions/2969870/removing-minimize-maximize-buttons-in-tkinter
#https://thispointer.com/python-convert-list-of-lists-or-nested-list-to-flat-list/
#https://stackoverflow.com/questions/18265935/how-do-i-create-a-list-with-numbers-between-two-values
#https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop

#https://stackoverflow.com/questions/2261191/how-can-i-put-2-buttons-next-to-each-other
#https://stackoverflow.com/questions/68327/change-command-method-for-tkinter-button-in-python
#https://www.geeksforgeeks.org/queue-in-python/
#https://stackoverflow.com/questions/53580507/disable-enable-button-in-tkinter
#https://www.tutorialspoint.com/python/tk_text.html
#https://www.geeksforgeeks.org/stack-in-python/
#https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
#https://stackoverflow.com/questions/22720843/how-to-center-a-widget-vertically-in-tkinter
#https://stackoverflow.com/questions/24756712/deepcopy-is-extremely-slow/29385667#29385667
#https://stackoverflow.com/questions/11949391/how-do-i-use-tkinter-to-create-line-wrapped-text-that-fills-the-width-of-the-win
#https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment
#https://www.geeksforgeeks.org/python-askopenfile-function-in-tkinter/?ref=lbp
#https://stackoverflow.com/questions/6085467/python-min-function-with-a-list-of-objects