from tkinter import *

class Board:

    def __init__(self, boardDimensions = None):
        #   The global window
        self.root = Tk()

        #   Load various pieces
        self.dark_green = PhotoImage(file = "images/dark_green_piece.png")
        self.light_green = PhotoImage(file="images/light_green_piece.png")
        self.dark_red = PhotoImage(file="images/dark_red_piece.png")
        self.light_red = PhotoImage(file = "images/light_red_piece.png")
        self.empty = PhotoImage(file="images/empty_square.png")

        #   The frames that hold all the content for the window
        self.notificationFrame = Frame(self.root, height=50)
        self.boardFrame = Frame(self.root)

        #   Initialize the turn to green by default
        self.turn = "green"

        if boardDimensions == None:
                return

        self.dimen = boardDimensions

        #   Set the notification bar to welcome the players
        var = StringVar()
        self.notification = Label(self.notificationFrame, textvariable=var)
        var.set("Hello welcome to Halma")
        self.notification.pack()
        self.notificationFrame.grid(row=0)

        self.buttonJustClicked = None

        #   Initialize the board to the dimensions specified
        self.listBoard = [[None, ""] for i in range(self.dimen*self.dimen)]
        self.boardFrame.grid(row=1)
        self.boardFrame.config(bg='black')
        for row in range(1, self.dimen + 1):
            for column in range(self.dimen):

                #   Create all the buttons for the board
                button = Button(self.boardFrame)
                button.grid(row=row, column=column)
                button.text = str(row-1) +","+ str(column)   #The text field is how we will keep track of the status of each button
                button.config(image=self.empty, width="100", height="100")
                button.bind("<Button-1>", self.handleClick)
                self.listBoard[((row-1) * self.dimen) + column][0] = button
                self.listBoard[((row-1) * self.dimen) + column][1] = "empty"

        self.setPieces(19)
        self.root.mainloop()

# @brief    The is the default method that is attached to a square
#
# @details  When the board is created and all the squares are just blank grey squares,
#           this method is set as the event that is called when it is clicked.
#
# @param[in]    event
#               The event object after a click has occurred containing the Button widget
#                   of the button that was just clicked
    def handleClick(self, event):
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        #   If there was a valid piece that was clicked one click before this,
        #       we are assuming the piece want's to be moved.  So we check if
        #       it legal and send it off for the piece to be moves.
        if self.buttonJustClicked is not None:
            oldxy = self.buttonJustClicked.text.split(",")
            oldx = int(oldxy[0])
            oldy = int(oldxy[1])
            legalMoves = self.generateLegalMoves(oldx, oldy)
            if [x,y] in legalMoves:
                print("legal move")
                self.handlePieceClick(event)
            else:
                print("illegal move")
                self.listBoard[oldx * self.dimen + oldy][1] = "green"
                self.listBoard[oldx * self.dimen + oldy][0].config(bg='white')
                self.buttonJustClicked = None




        #self.handleGreenClick(event)
        print(event.widget.text)

# @brief    sets all the pieces on the board
#
# @details  this will work for any number of pieces given that you specify how many row
#               some number of pieces produces.  If this needed to be completely portable
#               there could be some math added but that is unnecessary for our application
#
# @param[in]    numPieces
#               - an integer containing the number of pieces that each team should have
    def setPieces(self, numPieces):

        self.numPieces = numPieces
        if(numPieces == 19):
            numRows = 5

        #   Set the green pieces
        for row in range(numRows):
            if row == 0 or row == 1:
                for column in range(numRows):
                    self.listBoard[row * self.dimen + column][0].image = self.dark_green
                    self.listBoard[row * self.dimen + column][0].bind("<Button-1>", self.handlePieceClick)
                    self.listBoard[row * self.dimen + column][0].config(image=self.dark_green)
                    self.listBoard[row * self.dimen + column][1] = "green"
            else:
                for column in range(numRows - row + 1):
                    self.listBoard[row * self.dimen + column][0].image = self.dark_green
                    self.listBoard[row * self.dimen + column][0].bind("<Button-1>", self.handlePieceClick)
                    self.listBoard[row * self.dimen + column][0].config(image=self.dark_green)
                    self.listBoard[row * self.dimen + column][1] = "green"

        #   Set the red pieces
        tempNumRows = self.dimen - numRows + 1
        for row in range(self.dimen - 1, self.dimen - numRows - 1, -1):

            if row == self.dimen - 1 or row == self.dimen - 2:
                for column in range(self.dimen - numRows, self.dimen):
                    self.listBoard[row * self.dimen + column][0].image = self.dark_red
                    self.listBoard[row * self.dimen + column][0].bind("<Button-1>", self.handlePieceClick)
                    self.listBoard[row * self.dimen + column][0].config(image=self.dark_red)
                    self.listBoard[row * self.dimen + column][1] = "red"
            else:
                print(tempNumRows)
                for column in range(tempNumRows, self.dimen):
                    self.listBoard[row * self.dimen + column][0].image = self.dark_red
                    self.listBoard[row * self.dimen + column][0].bind("<Button-1>", self.handlePieceClick)
                    self.listBoard[row * self.dimen + column][0].config(image=self.dark_red)
                    self.listBoard[row * self.dimen + column][1] = "red"
                tempNumRows+=1

# @brief    checks the current board to see if either team has won
#
# @details  converted from the code for setting the pieces so if another piece configuration was added
#               the support would also have to be added here
#
# @param[out]   string
#               "red" if red won    "green" if green won    "none" if neither team won
#
#
    def isWin(self):
        if (self.numPieces == 19):
            numRows = 5

        #   Check to see if red has won
        winner = True
        for row in range(numRows):
            if row == 0 or row == 1:
                for column in range(numRows):
                    if self.listBoard[row * self.dimen + column][1] is not "red":
                        winner = False
                        break
            else:
                for column in range(numRows - row + 1):
                    if self.listBoard[row * self.dimen + column][1] is not "red":
                        winner = False
                        break
            if not winner:
                break
        if winner:
            return "red"

        winner = True

        #   Check to see if green won
        tempNumRows = self.dimen - numRows + 1
        for row in range(self.dimen - 1, self.dimen - numRows - 1, -1):
            if row == self.dimen - 1 or row == self.dimen - 2:
                for column in range(self.dimen - numRows, self.dimen):
                    if self.listBoard[row * self.dimen + column][1] is not "green":
                        winner = False
                        break
            else:
                for column in range(tempNumRows, self.dimen):
                    if self.listBoard[row * self.dimen + column][1] is not "green":
                        winner = False
                        break
                tempNumRows += 1
            if not winner:
                break

        if winner:
            return "green"
        else:
            return "none"


# @brief    the method attached to a tile containing a piece
#
# @details  When setting the pieces this method is set as the event listener for each piece
#           whether it is green or red.  There is functionality built in to handle turn taking,
#           and security to make sure you can't set a piece on another piece
#
# @param[in]    event
#               An Event object containing the Button widget that was just clicked
    def handlePieceClick(self, event):
        print("Handling", self.turn, "click")
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        #   If the tile just clicked is the correct color for whose turn it is
        if self.listBoard[x * self.dimen + y][1] is self.turn and self.buttonJustClicked is None:
            self.listBoard[x * self.dimen + y][1] = "selected"
            self.listBoard[x * self.dimen + y][0].config(bg = 'blue')
            self.buttonJustClicked = self.listBoard[x * self.dimen + y][0]
            print("Selected a ",self.turn," piece")
        #   If there already was a piece selected...
        elif self.buttonJustClicked is not None:
            oldXY = self.buttonJustClicked.text.split(",")
            oldX = int(oldXY[0])
            oldY = int(oldXY[1])
            #   we have to make sure the space isn't occupied...
            if self.listBoard[x *self.dimen + y][1] is not "empty":
                print("There is already a piece there")
                #   Unselecting the button
                self.listBoard[oldX * self.dimen + oldY][0].config(bg = 'white')
                self.listBoard[oldX * self.dimen + oldY][1] = self.turn
                self.buttonJustClicked = None
            #   and if it isn't we can go ahead and make the move
            else:
                print("handling making teh selection")
                #   Getting rid of old tile
                self.listBoard[oldX * self.dimen + oldY][1] = "empty"
                self.listBoard[oldX * self.dimen + oldY][0].image = self.empty
                self.listBoard[oldX * self.dimen + oldY][0].config(image = self.empty, bg = 'white')
                self.listBoard[oldX * self.dimen + oldY][0].bind("<Button-1>", self.handleClick)

                #   Changind the new square to the piece
                if self.turn is "green":
                    self.listBoard[x * self.dimen + y][0].image = self.dark_green
                    self.listBoard[x * self.dimen + y][0].config(image = self.dark_green)
                else:
                    self.listBoard[x * self.dimen + y][0].image = self.dark_red
                    self.listBoard[x * self.dimen + y][0].config(image=self.dark_red)

                self.listBoard[x * self.dimen + y][0].bind("<Button-1>", self.handlePieceClick)
                self.listBoard[x * self.dimen + y][1] = self.turn
                self.buttonJustClicked = None

                if self.turn is "green":
                    self.turn = "red"
                else:
                    self.turn = "green"

# @brief    takes in a coordinate and generates all legal moves
#
# @param[in]    x
#               the x coordinate corresponding to the piece in question
#
# @param[in     y
#               the y coordinate corresponding to the piece in question
#
# @param[out]   list
#               a list containing all legal moves
#
# @TODO         Convert to a set so that multiple values are not added
    def generateLegalMoves(self, x, y):
        legalMoves = []

        #   Find if the places around it are open
        for row in range(x-1, x+2):
            if row >= 0 and row < self.dimen:
                for column in range(y-1, y+2):
                    if column >= 0 and column < self.dimen:
                        #   If sn adjacent space is empty it is obvious we can move there
                        if self.listBoard[row * self.dimen + column][1] == "empty":
                            legalMoves.append([row, column])

                        #   If there is a piece there, we have to check for jumps
                        else:
                            self.findJumps([], legalMoves, x,y)

        print(legalMoves)
        return legalMoves

# @brief    finds all the possible moves a piece can make using jumps
#
# @param[in]    visited
#               a list containing all the already visited places
#
# @param[in]    legalMoves
#               a list containing all the legal moves found by jumping
#
# @param[in]    x
#               the x coordinate of the current location being looked at
#
# @param[in]    y
#               the y coordinate of teh current location being looked at
#
# @TODO         change all data structures to sets to increase lookup speed
    def findJumps(self, visited, legalMoves, x, y):
        visited.append([x,y])

        for rowOffset in range(-1,2):
            for columnOffset in range (-1,2):
                #   If the spot is in bounds and there is a piece to jump over...
                if self.isInBounds(x+rowOffset, y+columnOffset) and \
                                self.listBoard[(x+rowOffset) * self.dimen + (y+columnOffset)][1] is not "empty":
                    newX = x + (rowOffset*2)
                    newY = y + (columnOffset*2)
                    #   If the spot after the jump is in bounds and isn't already occupied...
                    if self.isInBounds(newX, newY) and self.listBoard[newX * self.dimen + newY][1] is "empty" and [newX, newY] not in visited:
                        legalMoves.append([newX, newY])
                        self.findJumps(visited, legalMoves, newX, newY)


    def isInBounds(self, x,y):
        if x<0 or x>= self.dimen or y<0 or y >=self.dimen:
            return False
        else:
            return True



board = Board(16)