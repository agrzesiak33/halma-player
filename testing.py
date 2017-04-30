from tkinter import *
import math


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
                button.text = str(row - 1) + "," + str(column) + ", 0"  # The text field contains the x y coordinates
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
                    #   Sets greens starting zone as reds safe zone.
                    self.allButtons[row * self.dimen + column].text = str(row) + "," + str(column) + ", 2"
                    self.listBoard[row * self.dimen + column] = 1
            else:
                for column in range(numRows - row + 1):
                    self.allButtons[row * self.dimen + column].image = self.dark_green
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_green)
                    self.allButtons[row * self.dimen + column].text = str(row) + "," + str(column) + ", 2"
                    self.listBoard[row * self.dimen + column] = 1

        # Set the red pieces
        tempNumRows = self.dimen - numRows + 1
        for row in range(self.dimen - 1, self.dimen - numRows - 1, -1):

            if row == self.dimen - 1 or row == self.dimen - 2:
                for column in range(self.dimen - numRows, self.dimen):
                    self.allButtons[row * self.dimen + column].image = self.dark_red
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_red)
                    self.allButtons[row * self.dimen + column].text = str(row) + "," + str(column) + ", 1"
                    self.listBoard[row * self.dimen + column] = 2
            else:
                print(tempNumRows)
                for column in range(tempNumRows, self.dimen):
                    self.allButtons[row * self.dimen + column].image = self.dark_red
                    self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                    self.allButtons[row * self.dimen + column].config(image=self.dark_red)
                    self.allButtons[row * self.dimen + column].text = str(row) + "," + str(column) + ", 1"
                    self.listBoard[row * self.dimen + column] = 2
                tempNumRows += 1
        for button in self.allButtons:
            print(button.text)

    def clearAvailableSpaces(self):
        for button in self.allButtons:
            xy = button.text.split(",")
            if self.listBoard[int(xy[0]) * self.dimen + int(xy[1])] == 0:
                button.image = self.empty
                button.config(image=self.empty)


class Halma:

# @brief    Sets up the board and other global variables
#
# @param[in]    playerConfig
#               a list containing two lists with information about whether each player is human or computer
#               playerConfig is of type: [[color : int, human/computer : int],...]
#               color:      1 for green     2 for red
#               human/AI:   1 for human     2 for computer
#
# @param[in]    boardSize
#               an optional argument with teh size of the board
#
# @param[in]    numPieces
#               an optional argument with the number of pieces for each team.  This needs to be a certain number
#                   or else the piece generation function will fail.  19 is standard for Halma but there will be
#                   support for more piece configurations in teh future
    def __init__(self, playerConfig, boardSize = 15, numPieces=19):
        self.dimen = boardSize
        self.numPieces = numPieces
        self.turn = 1

        self.board = Board(boardSize, self.emptyButton, self.occupiedButton, numPieces)

        self.buttonJustClicked = None

        if playerConfig[0][1] is 2 or playerConfig[1][1] is 2:
            if playerConfig[0][1] is 2:
                self.computer = playerConfig[0][0]
            elif playerConfig[1][1] is 2:
                self.computer = playerConfig[1][0]

        print(self.generateAllLegalMoves(self.turn, self.board.listBoard))
        # self.board.root.mainloop()

    def play(self, playerColor):

        #   Make the color of the player

        while True:
            self.board.root.update_idletasks()
            self.board.root.update()

            try:
                self.computer
                #   If it is the computers turn we have to find his move and make it
                if self.computer is self.turn:
                    pathToBestBoard = self.findNextMove(0, self.turn)
                    pieceToMove = pathToBestBoard[0]
                    spaceToMoveTo = pathToBestBoard[1]

                    self.movePiece(pieceToMove[0], pieceToMove[1], spaceToMoveTo[0], spaceToMoveTo[1])

            except AttributeError:
                pass


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

                    self.movePiece(oldX, oldY, x, y, self.turn)

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

    def movePiece(self, oldX, oldY, newX, newY, turn):
        print("Moving the piece")
        #   Getting rid of old tile
        self.board.listBoard[oldX * self.dimen + oldY] = 0
        self.board.allButtons[oldX * self.dimen + oldY].config(bg='white')
        self.board.allButtons[oldX * self.dimen + oldY].bind("<Button-1>", self.emptyButton)

        #   Changing the new square to the piece
        #   Also adds a marker to show where the piece came from
        if self.turn is 1:
            self.board.allButtons[newX * self.dimen + newY].image = self.board.dark_green
            self.board.allButtons[newX * self.dimen + newY].config(image=self.board.dark_green)

            self.board.allButtons[oldX * self.dimen + oldY].image = self.board.light_green
            self.board.allButtons[oldX * self.dimen + oldY].config(image=self.board.light_green)
        else:
            self.board.allButtons[newX * self.dimen + newY].image = self.board.dark_red
            self.board.allButtons[newX * self.dimen + newY].config(image=self.board.dark_red)

            self.board.allButtons[oldX * self.dimen + oldY].image = self.board.light_red
            self.board.allButtons[oldX * self.dimen + oldY].config(image=self.board.light_red)

        self.board.allButtons[newX * self.dimen + newY].bind("<Button-1>", self.occupiedButton)
        self.board.listBoard[newX * self.dimen + newY] = self.turn
        self.buttonJustClicked = None

        #print(self.board.listBoard)
        #   If we are here a valid move just happened and now we check to see if anyone won.
        if self.isWin(self.board.listBoard) is not "none":
            print(self.isWin(self.board.listBoard))
            self.board.notification.config(text=self.isWin(self.board.listBoard) + " won!")
            self.board.notification.pack()

        #   moves the turn to the other person
        if self.turn is 1:
            self.turn = 2
        else:
            self.turn = 1




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
                            #   Checking to make sure that we don't enter our base again
                            if self.turn == 1 and self.board.allButtons[row * dimen + column].text[-1] != str(2):
                                append([row, column])
                            elif self.turn == 2 and self.board.allButtons[row * dimen + column].text[-1] != str(1):
                                append([row, column])
                        # If there is a piece there, we have to check for jumps
                        else:
                            self.findJumps([], legalMoves, board, x, y)

        #   Per the game instructions, once a piece enters their safe zone it can't leave
        #   This probably needs to be sped up a ton
        if self.board.allButtons[x * dimen + y].text[-1] != "0":
            print(self.board.allButtons[x * dimen + y].text[-1])
            print("before removals: ")
            print(legalMoves)
            if self.board.allButtons[x * dimen + y].text[-1] == str(self.turn):
                legalEndMove = []
                for move in legalMoves:
                    if self.board.allButtons[move[0] * dimen + move[1]].text[-1] == str(self.turn):
                        print(move, " works")
                        legalEndMove.append(move)





        try:
            legalEndMove
            print(legalEndMove)
            return legalEndMove
        except UnboundLocalError:
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
#
# @param[out]   a list containing all possible moves
#               has the format [[pieceX, pieceY,[[possX, possY], [possX, possY]...]]...]
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
    def isWin(self, board):
        # if (self.numPieces == 19):
        numRows = 2

        #   Check to see if red has won
        winner = True
        for row in range(numRows):
            if row == 0 or row == 1:
                for column in range(numRows):
                    if board[row * self.dimen + column] is not 2:
                        winner = False
                        break
            else:
                for column in range(numRows - row + 1):
                    if board[row * self.dimen + column] is not 2:
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

# @brief    Looks over the board and using MiniMax search with aplha beta pruning,
#               returns the best move within a given time.
#
# @param[in]    time
#               the amount of time we are allowed
#
# @param[in]    turn
#               an integer corresponding to whose turn it is
#               1 for green     2 for red
#
# @param[out]   a list containing the
#
    def findNextMove(self, time, turn):
        #   Convert the inefficient representation of the board into a better one to pass around
        board = self.board.listBoard
        currentMax = []
        if turn is 1:
            opposingTurn = 2
        else:
            opposingTurn = 1
        for piece in range(self.dimen):
            if board[piece] is turn:
                moveMin = self.Min(board, opposingTurn, turn, 5, [int(piece/self.dimen), piece % self.dimen])
                if moveMin[1] > currentMax[1]:
                    currentMax = moveMin

        return currentMax[0]



# @brief    determines the absolute best move possible
#
# @param[in]    board
#               a dictionary representation of the board
#
# @param[in]    turn
#               an interger corresponding to whose turn it is as this level
#               1 for green     2 for red
#
# @param[in]    opposingTurn
#               an integer corresponding to whose turn it will be next turn
#
# @param[in]    depth
#               the current remaining iterations
#
# @param[in]    path
#               a list containing the path so far
#
# @param[in]    alpha
#               an integer representing the best value that the maximizer has found in the current path from the root
#
# @param[in]    beta
#               an integer representing the best value that the minimizer has found in teh current path from the root
#
# @param[out]   a list containing the path so far as well as the goodness of this state
#               [ path : list, goodness : integer]
#               path is of the form:  [[startX, startY], [moveX, moveY],...]
    def Max(self, board, turn, opposingTurn, depth, path, alpha, beta):
        if depth <= 0:
            #   TODO    call the to be made eval function with turn is the turn parameter in the function
            #       we would be calling eval with turn in this case because if we are out of depth,
            #           that means that Min (red) is calling this function and min (red) selects the worst
            #           possible move for green and not necessarily the one that helps red the most
            return [path, 0]
        else:
            localPath = path
            localBoard = board
            currentMax = [[], -math.inf]    # [0] is the path of the best score : list     [1] is the score itself : int
            #   All moves is in the form: [[oldX, oldY, [[possX, possY],...],...]
            allMoves = self.generateAllLegalMoves(turn, board)
            for moveSet in allMoves:
                for move in moveSet[2]:
                    #   Set old space to empty
                    localBoard[moveSet[0 * self.dimen + moveSet[1]]] = 0

                    #   Move the space on the localBoard
                    localBoard[move[0] * self.dimen + move[1]] = turn

                    localPath.append(move)

                    #   Calculate one of the min values coming back and reset variables
                    moveMin = self.Max(localBoard, opposingTurn, turn, depth - 1, localPath, alpha, beta)

                    #   Pruning is the found value is larger than the best current value for the minimizer node (beta)
                    if moveMin[1] >= beta:
                        return moveMin

                    if moveMin[1] > alpha:
                        alpha = moveMin[1]

                    if moveMin[1] < currentMax[1]:
                        currentMax = moveMin

                    localPath = path
                    localBoard = board

            #   We have to take care of the case where there are no legal moves for the player which
            #       would mean he is the winner and this needs to return the maximum possible score.
            #   TODO    replace these placeholder strings with either an array with passed in path and highest score
            #   TODO    or the score we found above from calling the min function
            if currentMax == -math.inf:
                #   If this is reached, it means max (green) has no moves to make which means green has won and so
                #       we signal this with teh highest possible score
                return "The max score"
            else:
                return "the score that we found from calling min"



# @brief    determines the absolute worst move possible for Max
#
# @param[in]    board
#               a dictionary representation of the board
#
# @paran[in]    turn
#               an interger corresponding to whose turn it is as the max level
#               1 for green     2 for red
#
# @param[in]    opposingTurn
#               an integer corresponding to whose turn it will be next turn
#
# @paran[in]    depth
#               the current remaining iterations
#
# @param[in]    path
#               a list containing the path so far
#
# @param[in]    alpha
#               an integer representing the best value that the maximizer has found in the current path from the root
#
# @param[in]    beta
#               an integer representing the best value that the minimizer has found in teh current path from the root
#
# @param[out]   a list containing the path so far as well as the goodness of this state
#               [ path : list, goodness : integer]
#               path is of the form:  [[startX, startY], [moveX, moveY],...]
    def Min(self, board, turn, opposingTurn, depth, path, alpha, beta):
        if depth <= 0:
            #   TODO     call the to be made eval function with opposingTurn is the turn parameter in the function
            #       we would be calling eval with opposingTurn in this case because if we are out of depth,
            #           that means that Max (green) is calling this function and so we have to return the board
            #           evaluation with respect green.
            return [path, 0]
        else:
            localPath = path
            localBoard = board
            currentMin = [[], math.inf]  # [0] is the path of the best score : list    [1] is the score itself : int
            #   allMoves is in the form: [[oldX, oldY, [[possX, possY],...],...]
            allMoves = self.generateAllLegalMoves(turn, board)
            for moveSet in allMoves:
                for move in moveSet[2]:
                    #   Set old space to empty
                    localBoard[moveSet[0 * self.dimen + moveSet[1]]] = 0

                    #   Move the space on the localBoard
                    localBoard[move[0] * self.dimen + move[1]] = turn

                    localPath.append(move)

                    #   Calculate one of the min values coming back and reset variables
                    moveMin = self.Max(localBoard, opposingTurn, turn, depth - 1, localPath, alpha, beta)

                    #   Pruning if the found value is less than the current best value for the maximizer node (alpha)
                    if moveMin[1] <= alpha:
                        return moveMin

                    if moveMin[1] < beta:
                        beta = moveMin[1]

                    if moveMin[1] < currentMin[1]:
                        currentMin = moveMin

                    localPath = path
                    localBoard = board

            #   TODO    replace these placeholder strings with either an array with passed in path and highest score
            #   TODO    or the score we found above from calling the min function
            if currentMin == math.inf:
                #   If this is reached, min (red) has no move to make which means they won the game so we have
                #       signal this by returning the lowest possible score.
                return "The lowest possible score"
            else:
                return "the score that we found from calling max"

halma = Halma([[1, 1], [2, 1]], 4)
halma.play()

#   TODO    INTEGRATE THE UTILITY FUNCTION INTO MIN AND MAX
#   TODO    implement a time limit into minimax
#   TODO    make findNextMove use IDS
#   TODO    add analytics into minimax
#   TODO    add logic code to highlight the piece that just moved not just where it came from
#   TODO    make the UI update with "I'm thinking" with a timer with the time remaining
#   TODO    once someone wins, display the number of moves made and teh final score
#               the score is +1 for each piece in the camp + 1/d for each piece outside where d = shortest distance from
#                   the piece to the base
#   TODO    add a notification that is the humans turn when applicable
