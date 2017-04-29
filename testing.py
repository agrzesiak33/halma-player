from tkinter import *


class Board:
    def __init__(self, boardDimensions, emptyFunction, occupiedFunction, numPieces=19):
        self.root = Tk()

        #   Load various pieces
        self.dark_green = PhotoImage(file="images/dark_green_piece.png")
        self.light_green = PhotoImage(file="images/light_green_piece.png")
        self.dark_red = PhotoImage(file="images/dark_red_piece.png")
        self.light_red = PhotoImage(file="images/light_red_piece.png")
        self.empty = PhotoImage(file="images/empty_square.png")
        self.available = PhotoImage(file="images/available.png")

        #   The frames that hold all the content for the window
        self.notificationFrame = Frame(self.root, height=50)
        self.boardFrame = Frame(self.root)

        self.dimen = boardDimensions

        #   Set the notification bar to welcome the players
        self.notification = Label(self.notificationFrame, text="Welcome to Halma")
        self.notification.pack()
        self.notificationFrame.grid(row=0)

        self.buttonJustClicked = None

        #   Initialize the board to the dimensions specified
        self.allButtons = []
        self.listBoard = {}

        self.greenPieces = []
        self.redPieces = []

        self.boardFrame.grid(row=1)
        self.boardFrame.config(bg='black')

        #   Creating all the empty spaces for the board
        for row in range(1, self.dimen + 1):
            for column in range(self.dimen):
                button = Button(self.boardFrame)
                button.grid(row=row, column=column)
                button.text = str(row - 1) + "," + str(column)  # The text field contains the x y coordinates
                button.config(image=self.empty, width="100", height="100")
                button.bind("<Button-1>", emptyFunction)
                self.allButtons.append(button)
                self.listBoard[((row - 1) * self.dimen) + column] = 0

        self.numPieces = numPieces
        # if (numPieces == 19):
        numRows = 2

        # Set the green pieces
        for row in range(numRows):
            if row == 0 or row == 1:
                for column in range(numRows):
                    self.allButtons[row * self.dimen + column].image = self.dark_green
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_green)
                    self.listBoard[row * self.dimen + column] = 1
                    self.greenPieces.append([row, column])
            else:
                for column in range(numRows - row + 1):
                    self.allButtons[row * self.dimen + column].image = self.dark_green
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_green)
                    self.listBoard[row * self.dimen + column] = 1
                    self.greenPieces.append([row, column])

        # Set the red pieces
        tempNumRows = self.dimen - numRows + 1
        for row in range(self.dimen - 1, self.dimen - numRows - 1, -1):

            if row == self.dimen - 1 or row == self.dimen - 2:
                for column in range(self.dimen - numRows, self.dimen):
                    self.allButtons[row * self.dimen + column].image = self.dark_red
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_red)
                    self.listBoard[row * self.dimen + column] = 2
                    self.redPieces.append([row, column])
            else:
                print(tempNumRows)
                for column in range(tempNumRows, self.dimen):
                    self.allButtons[row * self.dimen + column].image = self.dark_red
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_red)
                    self.listBoard[row * self.dimen + column] = 2
                    self.redPieces.append([row, column])
                tempNumRows += 1

    def clearAvailableSpaces(self):
        for button in self.allButtons:
            xy = button.text.split(",")
            if self.listBoard[int(xy[0]) * self.dimen + int(xy[1])] == 0:
                button.image = self.empty
                button.config(image=self.empty)


class Halma:
    def __init__(self, boardSize, numPieces=19):
        self.dimen = boardSize
        self.numPieces = numPieces
        self.turn = 1

        self.board = Board(boardSize, self.emptyButton, self.occupiedButton, numPieces)

        self.buttonJustClicked = None

        print(self.generateAllLegalMoves(self.turn, self.board.allButtons))
        # self.board.root.mainloop()

    def play(self, playerColor):

        #   Make the color of the player

        while True:
            self.board.root.update_idletasks()
            self.board.root.update()

# @brief    Handles the clicked events where there is no piece on the tile
#
# @details  When the board is created and all the squares are just blank grey squares,
#           this method is set as the event that is called when it is clicked.
#
# @param[in]    event
#               The event object after a click has occurred containing the Button widget
#                   of the button that was just clicked
    def emptyButton(self, event):
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        #   If there was a valid piece that was clicked one click before this,
        #       we are assuming the piece want's to be moved.  So we check if
        #       it legal and send it off for the piece to be moves.
        if self.buttonJustClicked is not None:
            oldxy = self.buttonJustClicked.text.split(",")
            oldX = int(oldxy[0])
            oldY = int(oldxy[1])
            legalMoves = self.generateLegalMoves(oldX, oldY, self.board.listBoard)
            self.board.clearAvailableSpaces()
            if [x, y] in legalMoves:
                print("legal move")
                #   we have to make sure the space isn't occupied...
                if self.board.listBoard[x * self.dimen + y] is not 0:
                    print("There is already a piece there")
                    #   Deselecting the button and clear the available markers
                    self.board.allButtons[oldX * self.dimen + oldY].config(bg='white')
                    self.board.listBoard[oldX * self.dimen + oldY] = self.turn
                    self.buttonJustClicked = None
                    self.board.clearAvailableSpaces()
                # and if it isn't we can go ahead and make the move
                else:
                    print("handling making teh selection")
                    #   Getting rid of old tile
                    self.board.listBoard[oldX * self.dimen + oldY] = 0
                    self.board.allButtons[oldX * self.dimen + oldY].config(bg='white')
                    self.board.allButtons[oldX * self.dimen + oldY].bind("<Button-1>", self.emptyButton)

                    #   Changing the new square to the piece
                    #   Also adds a marker to show where the piece came from
                    if self.turn is 1:
                        self.board.allButtons[x * self.dimen + y].image = self.board.dark_green
                        self.board.allButtons[x * self.dimen + y].config(image=self.board.dark_green)

                        self.board.allButtons[oldX * self.dimen + oldY].image = self.board.light_green
                        self.board.allButtons[oldX * self.dimen + oldY].config(image=self.board.light_green)
                    else:
                        self.board.allButtons[x * self.dimen + y].image = self.board.dark_red
                        self.board.allButtons[x * self.dimen + y].config(image=self.board.dark_red)

                        self.board.allButtons[oldX * self.dimen + oldY].image = self.board.light_red
                        self.board.allButtons[oldX * self.dimen + oldY].config(image=self.board.light_red)

                    self.board.allButtons[x * self.dimen + y].bind("<Button-1>", self.occupiedButton)
                    self.board.listBoard[x * self.dimen + y] = self.turn
                    self.buttonJustClicked = None

                    #   If we are here a valid move just happened and now we check to see if anyone won.
                    if self.isWin() is not "none":
                        print(self.isWin())
                        self.board.notification['text'] = "You won!"
                        self.board.notification.config(text=self.isWin() + " won!")
                        self.board.notification.pack()
                        exit()

                    # Remove teh old position from the player piece list and add the new one
                    #   Also moves teh turn to the other person
                    if self.turn is 1:
                        self.board.greenPieces.remove([oldX, oldY])
                        self.board.greenPieces.append([x, y])
                        self.turn = 2
                    else:
                        self.board.redPieces.remove([oldX, oldY])
                        self.board.redPieces.append([x, y])
                        self.turn = 1
            else:
                print("illegal move")
                self.board.listBoard[oldX * self.dimen + oldY] = self.turn
                self.board.allButtons[oldX * self.dimen + oldY].config(bg='white')
                self.buttonJustClicked = None

# @brief    Handles the clicked events where there is a piece on the tile
#
#
# @details  When setting the pieces this method is set as the event listener for each piece
#           whether it is green or red.  There is functionality built in to handle turn taking,
#           and security to make sure you can't set a piece on another piece
#
# @param[in]    event
#               An Event object containing the Button widget that was just clicked
    def occupiedButton(self, event):
        print("Handling", self.turn, "click")
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        #   If the tile just clicked is the correct color for whose turn it is
        if self.board.listBoard[x * self.dimen + y] is self.turn and self.buttonJustClicked is None:
            #   Save this button that was just selected and show it was selected
            self.board.listBoard[x * self.dimen + y] = -1
            self.board.allButtons[x * self.dimen + y].config(bg='blue')
            self.buttonJustClicked = self.board.allButtons[x * self.dimen + y]
            #   Get it's available moves and highlight them as available
            availableMoves = self.generateLegalMoves(x, y, self.board.listBoard)
            for move in availableMoves:
                self.board.allButtons[move[0] * self.dimen + move[1]].image = self.board.available
                self.board.allButtons[move[0] * self.dimen + move[1]].config(image=self.board.available)

            print("Selected a ", self.turn, " piece")
        # If either the tile is of teh wrong color
        #   Or the same piece that was selected one click before is clicked again
        #   Unhighlight the board and clear the variable holding the selected button
        else:
            self.board.clearAvailableSpaces()
            self.board.allButtons[x * self.dimen + y].config(bg='white')
            self.board.listBoard[x * self.dimen + y] = self.turn
            self.buttonJustClicked = None

# @brief    takes in a coordinate and generates all legal moves
#
# @param[in]    x
#               the x coordinate corresponding to the piece in question
#
# @param[in     y
#               the y coordinate corresponding to the piece in question
#
# @param[in]    board
#               a dictionary containing the board
#
# @param[out]   list
#               a list containing all legal moves
    def generateLegalMoves(self, x, y, board):
        legalMoves = []
        append = legalMoves.append
        dimen = self.dimen

        #   Find if the places around it are open
        for row in range(x - 1, x + 2):
            if 0 <= row < dimen:
                for column in range(y - 1, y + 2):
                    if 0 <= column < dimen:
                        #   If an adjacent space is empty it is obvious we can move there
                        if board[row * dimen + column] == 0 and [row, column] not in legalMoves:
                            append([row, column])

                        # If there is a piece there, we have to check for jumps
                        else:
                            self.findJumps([], legalMoves, board, x, y)

        print(legalMoves)
        return legalMoves

# @brief    Generates all the legal moves on the board given whose turn it is
#
# @param[in]    turn
#               an int designating whose turn it is
#               1 for green
#               2 for red
#
# @param[in]    board
#               a dictionary containing the
    def generateAllLegalMoves(self, turn, board):
        allLegalMoves = []
        append = allLegalMoves.append

        for x in range(self.dimen):
            for y in range(self.dimen):
                if board[x * self.dimen + y] == turn:
                    append([x, y, self.generateLegalMoves(x, y, board)])
        return allLegalMoves

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
#               the y coordinate of the current location being looked at
    def findJumps(self, visited, legalMoves, board, x, y):
        visited.append([x, y])
        append = legalMoves.append

        for rowOffset in range(-1, 2):
            for columnOffset in range(-1, 2):
                #   If the adjacent spot is in bounds and there is a piece to jump over...
                if self.isInBounds(x + rowOffset, y + columnOffset) and \
                                board[(x + rowOffset) * self.dimen + (y + columnOffset)] is not 0:
                    newX = x + (rowOffset + rowOffset)
                    newY = y + (columnOffset + columnOffset)
                    #   If the spot after the jump is in bounds and isn't already occupied...
                    if self.isInBounds(newX, newY) and board[newX * self.dimen + newY] is 0 \
                            and [newX, newY] not in visited and [newX, newY] not in legalMoves:
                        append([newX, newY])
                        self.findJumps(visited, legalMoves, board, newX, newY)

    def isInBounds(self, x, y):
        if x < 0 or x >= self.dimen or y < 0 or y >= self.dimen:
            return False
        else:
            return True

# @brief    checks the current board to see if either team has won
#
# @details  converted from the code for setting the pieces so if another piece configuration was added
#               the support would also have to be added here
#
# @param[out]   string
#               "red" if red won    "green" if green won    "none" if neither team won
# @TODO     Make this function so that it takes a board that is passed in
    def isWin(self):
        # if (self.numPieces == 19):
        numRows = 2

        #   Check to see if red has won
        winner = True
        for row in range(numRows):
            if row == 0 or row == 1:
                for column in range(numRows):
                    if self.board.listBoard[row * self.dimen + column] is not 2:
                        winner = False
                        break
            else:
                for column in range(numRows - row + 1):
                    if self.board.listBoard[row * self.dimen + column] is not 2:
                        winner = False
                        break
            if not winner:
                break
        if winner:
            return "Red"

        winner = True

        #   Check to see if green won
        tempNumRows = self.dimen - numRows + 1
        for row in range(self.dimen - 1, self.dimen - numRows - 1, -1):
            if row == self.dimen - 1 or row == self.dimen - 2:
                for column in range(self.dimen - numRows, self.dimen):
                    if self.board.listBoard[row * self.dimen + column] is not 1:
                        winner = False
                        break
            else:
                for column in range(tempNumRows, self.dimen):
                    if self.board.listBoard[row * self.dimen + column] is not 1:
                        winner = False
                        break
                tempNumRows += 1
            if not winner:
                break

        if winner:
            return "Green"
        else:
            return "none"


halma = Halma(5)
halma.play("green")
