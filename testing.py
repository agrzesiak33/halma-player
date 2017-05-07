from tkinter import *
import math
import time


class Board:
    def __init__(self, boardDimensions, emptyFunction, occupiedFunction, numPieces=19):
        self.root = Tk()

        #   Load various pieces
        self.dark_green = PhotoImage(file="images/dark_green_piece.png")
        self.light_green = PhotoImage(file="images/light_green_piece.png")
        self.dark_green_moved = PhotoImage(file="images/dark_green_piece_moved.png")
        self.dark_red = PhotoImage(file="images/dark_red_piece.png")
        self.light_red = PhotoImage(file="images/light_red_piece.png")
        self.dark_red_moved = PhotoImage(file="images/dark_red_piece_moved.png")
        self.empty = PhotoImage(file="images/empty_square.png")
        self.available = PhotoImage(file="images/available.png")

        #   Each bit in this board representation is a square on the board
        #   FYI When printing these representations, green is on the right red on the left (only on the start)
        self.allBoard = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.greenBoard = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.redBoard = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.redGoal = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.greenGoal = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.eitherGoal = 0b0000000000000000000000000000000000000000000000000000000000000000

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
        numRows = 4

        # Set the green pieces
        piecesInRow = 4
        for row in range(numRows):
            for column in range(piecesInRow):
                self.allButtons[row * self.dimen + column].image = self.dark_green
                self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                self.allButtons[row * self.dimen + column].config(image=self.dark_green)
                #   Sets greens starting zone as reds safe zone.
                self.allButtons[row * self.dimen + column].text = str(row) + "," + str(column) + ", 2"
                self.listBoard[row * self.dimen + column] = 1

                #   Using the new board representation
                self.allBoard |= (1 << (row * self.dimen + column))
                self.greenBoard |= (1 << (row * self.dimen + column))
                self.redGoal |= (1 << (row * self.dimen + column))
                self.eitherGoal |= (1 << (row * self.dimen + column))
            piecesInRow -= 1

        # Set the red pieces
        piecesInRow = 4
        for row in range(self.dimen - 1, self.dimen - numRows - 1, -1):
            for column in range(self.dimen - piecesInRow, self.dimen, 1):
                self.allButtons[row * self.dimen + column].image = self.dark_red
                self.allButtons[row * self.dimen + column].bind("<Button-1>", occupiedFunction)
                self.allButtons[row * self.dimen + column].config(image=self.dark_red)
                self.allButtons[row * self.dimen + column].text = str(row) + "," + str(column) + ", 1"
                self.listBoard[row * self.dimen + column] = 2

                #   Using the new board representation
                self.allBoard = self.allBoard | (1 << (row * self.dimen + column))
                self.redBoard |= (1 << (row * self.dimen + column))
                self.greenGoal |= (1 << (row * self.dimen + column))
            piecesInRow -= 1

#        for button in self.allButtons:
 #           print(button.text)
        #print(bin(self.allBoard))


    def cleanBoard(self):
        for button in self.allButtons:
            xy = button.text.split(",")
            if self.listBoard[int(xy[0]) * self.dimen + int(xy[1])] == 0:
                button.image = self.empty
                button.config(image=self.empty)
            elif self.listBoard[int(xy[0]) * self.dimen + int(xy[1])] == 1:
                button.image = self.dark_green
                button.config(image = self.dark_green)
            elif self.listBoard[int(xy[0]) * self.dimen + int(xy[1])] == 2:
                button.image = self.dark_red
                button.config(image=self.dark_red)

    def clearPieceClickListener(self, color):
        for piece in range(self.dimen * self.dimen):
            if self.listBoard[piece] == color:
                self.allButtons[piece].unbind('<Button-1>')


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
        self.numGreenMoves = 0
        self.numRedMoves = 0


        self.board = Board(boardSize, self.emptyButton, self.occupiedButton, numPieces)

        self.buttonJustClicked = None

        if playerConfig[0][1] is 2:
            self.computer = playerConfig[0][0]
            self.board.clearPieceClickListener(playerConfig[0][0])
        elif playerConfig[1][1] is 2:
            self.computer = playerConfig[1][0]
            self.board.clearPieceClickListener(playerConfig[1][0])

        #(self.generateAllLegalMoves(self.turn, self.board.listBoard))
        # self.board.root.mainloop()

    def play(self, turnTime):
        while True:
            self.board.root.update_idletasks()
            self.board.root.update()

            if self.isWin(self.board.greenBoard, self.board.greenGoal) is True:
                print("Green Won")
                break
            elif self.isWin(self.board.redBoard, self.board.redGoal) is True:
                print("Red won")
                break

            try:
                self.computer
                #   If it is the computers turn we have to find his move and make it
                if self.computer is self.turn:
                    #   Let the human know the computer is thinking
                    self.board.notification.config(text="Computer is thinking")
                    self.board.notification.pack()
                    self.board.root.update()

                    pathToBestBoard = self.findNextMove(turnTime, self.turn)
                    print("path: ", pathToBestBoard)
                    pieceToMove = pathToBestBoard[0][0]
                    spaceToMoveTo = pathToBestBoard[0][0]

                    self.movePiece(pieceToMove[0], pieceToMove[1], spaceToMoveTo[2], spaceToMoveTo[3])

                    #   Once the computer moved, we can let the human know it is their turn
                    self.board.notification.config(text="Hooman, it is your turn")
                    self.board.notification.pack()


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
            legalMoves = self.generateLegalMoves(oldX, oldY, self.board.allBoard)
            self.board.cleanBoard()
            if [x, y] in legalMoves:
                self.movePiece(oldX, oldY, x, y)
            else:
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
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        # self.board.cleanBoard()

        #   If the tile just clicked is the correct color for whose turn it is
        if self.buttonJustClicked is None and self.board.listBoard[x * self.dimen + y] is self.turn:
            #   Save this button that was just selected and show it was selected
            self.board.allButtons[x * self.dimen + y].config(bg='blue')
            self.buttonJustClicked = self.board.allButtons[x * self.dimen + y]
            #   Get it's available moves and highlight them as available
            availableMoves = self.generateLegalMoves(x, y, self.board.allBoard)
            for move in availableMoves:
                self.board.allButtons[move[0] * self.dimen + move[1]].image = self.board.available
                self.board.allButtons[move[0] * self.dimen + move[1]].config(image=self.board.available)

            # print("Selected a ", self.turn, " piece")
        # If either the tile is of the wrong color
        #   Or the same piece that was selected one click before is clicked again
        #   Unhighlight the board and clear the variable holding the selected button
        else:
            oldXY = self.buttonJustClicked.text.split(",")
            self.board.allButtons[int(oldXY[0]) * self.dimen + int(oldXY[1])].config(bg='white')
            self.buttonJustClicked = None
            self.board.cleanBoard()

    def movePiece(self, oldX, oldY, newX, newY):
        self.board.cleanBoard()
        #   Getting rid of old tile
        self.board.listBoard[oldX * self.dimen + oldY] = 0
        self.board.allButtons[oldX * self.dimen + oldY].config(bg='white')
        self.board.allButtons[oldX * self.dimen + oldY].bind("<Button-1>", self.emptyButton)
        #   Getting rid of old tile on new representation
        self.board.allBoard &= ~(1 << (oldX * self.dimen + oldY))
        if self.turn == 1:
            self.board.greenBoard &= ~(1 << (oldX * self.dimen + oldY))
        else:
            self.board.redBoard &= ~(1 << (oldX * self.dimen + oldY))


        #   Changing the new square to the piece
        #   Also adds a marker to show where the piece came from
        if self.turn is 1:
            self.board.allButtons[newX * self.dimen + newY].image = self.board.dark_green_moved
            self.board.allButtons[newX * self.dimen + newY].config(image=self.board.dark_green_moved)

            self.board.greenBoard |= (1 << (newX * self.dimen + newY))

            self.board.allButtons[oldX * self.dimen + oldY].image = self.board.light_green
            self.board.allButtons[oldX * self.dimen + oldY].config(image=self.board.light_green)

            self.numGreenMoves += 1

            if self.isWin(self.board.greenBoard, self.board.greenGoal):
                self.board.notification.config(text="Green won in " + str(self.numGreenMoves) + " moves")
                self.board.notification.pack()

        else:
            self.board.allButtons[newX * self.dimen + newY].image = self.board.dark_red_moved
            self.board.allButtons[newX * self.dimen + newY].config(image=self.board.dark_red_moved)

            self.board.redBoard |= (1 << (newX * self.dimen + newY))

            self.board.allButtons[oldX * self.dimen + oldY].image = self.board.light_red
            self.board.allButtons[oldX * self.dimen + oldY].config(image=self.board.light_red)

            self.numRedMoves += 1

            if self.isWin(self.board.redBoard, self.board.redGoal):
                self.board.notification.config(text="Red won in " + str(self.numRedMoves) + " moves")
                self.board.notification.pack()

        self.board.allButtons[newX * self.dimen + newY].bind("<Button-1>", self.occupiedButton)
        self.board.listBoard[newX * self.dimen + newY] = self.turn
        self.board.allBoard |= (1 << (newX * self.dimen + newY))
        self.buttonJustClicked = None

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
    def generateLegalMoves(self, x, y, allBoard):
        legalMoves = []
        append = legalMoves.append
        dimen = self.dimen

        #   Find if the places around it are open
        for row in range(x - 1, x + 2):
            if 0 <= row < dimen:
                for column in range(y - 1, y + 2):
                    if 0 <= column < dimen and (column is not y or row is not x):
                        #   If an adjacent space is empty...
                        if not allBoard & (1 << (row * dimen + column)) and [row, column] not in legalMoves:
                            #   If the piece is in either base...
                            if self.board.eitherGoal & (1 << (x * dimen + y)):
                                #   If the ending location is in a base...
                                if self.board.eitherGoal & (1 << (row * dimen + column)):
                                    #   We allow the move since a piece can move around a base once it gets there
                                    append([row, column])

                                #   If the ending position is not in a base
                                else:
                                    #   If it wants to leave its own base OK, if it wants to leave it's goal base NO
                                    if self.turn == 1 and self.board.redGoal & (1 << (x * dimen + y)):
                                        append([row, column])
                                    elif self.turn == 2 and self.board.greenGoal & (1 << (x * dimen + y)):
                                        append([row, column])


                            #   If the piece isn't in the base...
                            else:
                                #   If the potential move makes it in a base
                                if self.board.eitherGoal & (1 << (row * dimen + column)):
                                    #   If the piece wants to move in its goal base OK, in its own base NO
                                    if self.turn == 1 and self.board.greenGoal & (1 << (row * dimen + column)):
                                        append([row, column])
                                    elif self.turn == 2 and self.board.redGoal & (1 << (row * dimen + column)):
                                        append([row, column])
                                #   If the piece nor the potential move is in a base then we are fine
                                else:
                                    append([row, column])
                        # If there is a piece there, we have to check for jumps
                        else:
                            self.findJumps([], legalMoves, allBoard, x, y)

        #   Per the game instructions, once a piece enters their safe zone it can't leave
        #   This probably needs to be sped up a ton
        if self.board.allBoard & (1 << (x * dimen + y)):
            if self.board.allButtons[x * dimen + y].text[-1] == str(self.turn):
                legalEndMove = []
                for move in legalMoves:
                    if self.board.allButtons[move[0] * dimen + move[1]].text[-1] == str(self.turn):
                        legalEndMove.append(move)
        try:
            legalEndMove
            return legalEndMove
        except UnboundLocalError:
            return legalMoves

# @brief    Generates all the legal moves on the board given whose turn it is
#
# @param[in]    turn
#               an int designating whose turn it is
#               1 for green
#               2 for red
#
# @param[in]    board
#               an int containing the board for a specific player
#
# @param[out]   a list containing all possible moves
#               has the format [[pieceX, pieceY,[[possX, possY], [possX, possY]...]]...]
    def generateAllLegalMoves(self, allBoard, colorBoard):
        allLegalMoves = []
        append = allLegalMoves.append
        for x in range(self.dimen):
            for y in range(self.dimen):
                if colorBoard & (1 << (x * self.dimen + y)):

                    append([x, y, self.generateLegalMoves(x, y, allBoard)])
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
                                board & (1 << ((x + rowOffset) * self.dimen + (y + columnOffset))):
                    newX = x + (rowOffset + rowOffset)
                    newY = y + (columnOffset + columnOffset)
                    #   If the spot after the jump is in bounds and isn't already occupied...
                    if self.isInBounds(newX, newY) and not board & (1 << (newX * self.dimen + newY)) \
                            and [newX, newY] not in visited and [newX, newY] not in legalMoves:
                        append([newX, newY])
                        self.findJumps(visited, legalMoves, board, newX, newY)

    def isInBounds(self, x, y):
        if x < 0 or x >= self.dimen or y < 0 or y >= self.dimen:
            return False
        else:
            return True

# @brief    compares the current players board to their goal board to see if they won
#
# @param[in]    colorBoard
#               the integer representation of the board for one color
#
# @param[in]    colorGoal
#               the integer representation of the board for one color when all pieces are in the base
#
# @param[out]   True if the color won   False otherwise
    @staticmethod
    def isWin(colorBoard, colorGoal):

        if colorBoard is colorGoal:
            return True
        return False


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
# @param[out]   a list containing the path and score of the round
#
    def findNextMove(self, timeLimit, turn, allBoard=-1, greenBoard=-1, redBoard=-1):
        #   if allBoard is not -1 we are analyzing so we use the passed in boards instead
        if allBoard == -1:
            localAllBoard = self.board.allBoard
            localGreenBoard = self.board.greenBoard
            localRedBoard = self.board.redBoard
        else:
            localAllBoard = allBoard
            localGreenBoard = greenBoard
            localRedBoard = redBoard
        #   Convert the inefficient representation of the board into a better one to pass around
        currentMax = [[], -1]
        if turn is 1:
            opposingTurn = 2
        else:
            opposingTurn = 1

        endTime = time.time()
        endTime += timeLimit
        #(endTime)
        #print(time.time())
        for depth in range(3, 100):
            moveMax = self.Max(localAllBoard, localGreenBoard, localRedBoard, self.turn, opposingTurn, depth, [], -999999999, 999999999, endTime)

            #   If we are out of time, moveMax will come back with a value at index 2
            try:
                moveMax[2]
                if moveMax[1] > currentMax[1]:
                    return moveMax
                else:
                    return currentMax
            except (IndexError, TypeError) as e:
                pass
            print(moveMax)
            if moveMax[1] > currentMax[1]:
                currentMax = moveMax

        return currentMax



# @brief    determines the absolute best move possible
#
# @param[in]    board
#               an integer representation of the board
#
# @param[in]    turn
#               an integer corresponding to whose turn it is as this level
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
# @param[in]    endTime
#               the time in which we have to end searching
#
# @param[out]   a list containing the path so far as well as the goodness of this state
#               [ path : list, goodness : integer]
#               path is of the form:  [[startX, startY], [moveX, moveY],...]
    def Max(self, board, greenBoard, redBoard, turn, opposingTurn, depth, path, alpha, beta, endTime):
        #print("max depth: ", depth)
        #   First we make sure we have time to do more searching
        #   If we are out of time we return something different than usual
        #   TODO    call the to be eval function to get the goodness of this board and replace 99999999999 with it
        if time.time() > endTime:
            return [path, 999999999999, -1]

        if depth <= 0:
            #   TODO    call the to be made eval function with turn is the turn parameter in the function
            #       we would be calling eval with turn in this case because if we are out of depth,
            #           that means that Min (red) is calling this function and min (red) selects the worst
            #           possible move for green and not necessarily the one that helps red the most
            return [path, 0]
        else:
            localPath = list(path)
            localBoard = int(board)
            localGreen = int(greenBoard)
            localRed = int(redBoard)
            currentMax = [path, -999999999]   # [0] is the path of the best score : list   [1] is the score itself : int
            #   All moves is in the form: [[oldX, oldY, [[possX, possY],...],...]
            if turn == 1:
                allMoves = self.generateAllLegalMoves(board, greenBoard)
            else:
                allMoves = self.generateAllLegalMoves(board, redBoard)
            for moveSet in allMoves:
                for move in moveSet[2]:
                    #   Set old space to empty
                    #localBoard[moveSet[0] * self.dimen + moveSet[1]] = 0
                    localBoard &= ~(1 << (moveSet[0] * self.dimen + moveSet[1]))
                    #   Set the new piece
                    localBoard |= (1 << (move[0] * self.dimen + move[1]))
                    # localBoard[move[0] * self.dimen + move[1]] = turn

                    if turn == 1:
                        #   Clear the green board piece
                        localGreen &= ~(1 << (moveSet[0] * self.dimen + moveSet[1]))
                        #   Set the new piece
                        localGreen |= (1 << (move[0] * self.dimen + move[1]))
                    else:
                        #   Clear the red board piece
                        localRed &= ~(1 << (moveSet[0] * self.dimen + moveSet[1]))
                        #   Set the new piece
                        localRed |= (1 << (move[0] * self.dimen + move[1]))

                    localPath.append([moveSet[0], moveSet[1], move[0], move[1]])

                    #   Calculate one of the min values coming back and reset variables
                    moveMin = self.Min(localBoard, localGreen, localRed, opposingTurn, turn, depth - 1, localPath, alpha, beta, endTime)

                    #   Usually this try will fail but if it doesn't it means we're out of time and we return whatever
                    #       value we were working on
                    try:
                        moveMin[2]
                        if moveMin[1] > currentMax[1]:
                            return moveMin
                        else:
                            #   We have to make sure that the thing being returned has an index at 2
                            currentMax.append(-1)
                            return currentMax
                    except (IndexError, TypeError) as e:
                        pass

                    #   Pruning is the found value is larger than the best current value for the minimizer node (beta)
                    if moveMin[1] >= beta:
                        return moveMin

                    if moveMin[1] > alpha:
                        alpha = moveMin[1]

                    if moveMin[1] > currentMax[1]:
                        currentMax = moveMin

                    localPath = list(path)
                    localBoard = int(board)
                    localRed = int(redBoard)
                    localGreen = int(greenBoard)
            #print("after finding max: ", path, currentMax)
            #   We have to take care of the case where there are no legal moves for the player which
            #       would mean he is the winner and this needs to return the maximum possible score.
            return currentMax



# @brief    determines the absolute worst move possible for Max
#
# @param[in]    board
#               a dictionary representation of the board
#
# @param[in]    turn
#               an integer corresponding to whose turn it is as the max level
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
# @param[in]    endTime
#               the time in which we have to end searching
#
# @param[out]   a list containing the path so far as well as the goodness of this state
#               [ path : list, goodness : integer]
#               path is of the form:  [[startX, startY], [moveX, moveY],...]
    def Min(self, board, greenBoard, redBoard, turn, opposingTurn, depth, path, alpha, beta, endTime):
        #print("Min depth:, ",depth)
        #   First we make sure we have time to do more searching
        #   If we are out of time we return something different than usual
        #   TODO    call the to be eval function to get the goodness of this board and replace 99999999999 with it
        if time.time() > endTime:
            return [path, 999999999999, -1]


        if depth <= 0:
            #   TODO     call the to be made eval function with opposingTurn is the turn parameter in the function
            #       we would be calling eval with opposingTurn in this case because if we are out of depth,
            #           that means that Max (green) is calling this function and so we have to return the board
            #           evaluation with respect green.
            return [path, 0]
        else:
            localPath = list(path)
            localBoard = int(board)
            localGreen = int(greenBoard)
            localRed = int(redBoard)

            currentMin = [path, 999999999]  # [0] is the path of the best score : list    [1] is the score itself : int
            #   allMoves is in the form: [[oldX, oldY, [[possX, possY],...],...]
            if turn == 1:
                allMoves = self.generateAllLegalMoves(board, greenBoard)
            else:
                allMoves = self.generateAllLegalMoves(board, redBoard)
            for moveSet in allMoves:
                for move in moveSet[2]:

                    #   Set old space to empty
                    # localBoard[moveSet[0] * self.dimen + moveSet[1]] = 0
                    localBoard &= ~(1 << (moveSet[0] * self.dimen + moveSet[1]))
                    #   Set the new piece
                    localBoard |= (1 << (move[0] * self.dimen + move[1]))
                    # localBoard[move[0] * self.dimen + move[1]] = turn

                    if turn == 1:
                        #   Clear the green board piece
                        localGreen &= ~(1 << (moveSet[0] * self.dimen + moveSet[1]))
                        #   Set the new piece
                        localGreen |= (1 << (move[0] * self.dimen + move[1]))
                    else:
                        #   Clear the red board piece
                        localRed &= ~(1 << (moveSet[0] * self.dimen + moveSet[1]))
                        #   Set the new piece
                        localRed |= (1 << (move[0] * self.dimen + move[1]))

                    localPath.append([moveSet[0], moveSet[1], move[0], move[1]])

                    #   Calculate one of the min values coming back and reset variables
                    moveMax = self.Max(localBoard, localGreen, localRed, opposingTurn, turn, depth - 1, localPath, alpha, beta, endTime)

                    #   Usually this try will fail but if it doesn't it means we're out of time and we return whatever
                    #       value we were working on
                    try:
                        moveMax[2]
                        if moveMax[1] < currentMin[1]:
                            return moveMax
                        else:
                            #   We have to make sure that the thing being returned has an index at 2
                            currentMin.append(-1)
                            return currentMin
                    except (IndexError, TypeError) as e:
                        pass

                    #   Pruning if the found value is less than the current best value for the maximizer node (alpha)
                    if moveMax[1] <= alpha:
                        return moveMax

                    if moveMax[1] < beta:
                        beta = moveMax[1]

                    if moveMax[1] < currentMin[1]:
                        currentMin = moveMax

                    localPath = list(path)
                    localBoard = int(board)
                    localGreen = int(greenBoard)
                    localRed = int(redBoard)
            # print("after finding min: ", path, currentMin)

            #   TODO    replace these placeholder strings with either an array with passed in path and highest score
            #   TODO    or the score we found above from calling the min function
            return currentMin

    def analyzeMinimax(self):
        plysVSTime = dict()
        maxPlys = 0

        allBoard = 0b0000000000000000000000000000000000000000000000000000000000000000
        greenBoard = 0b0000000000000000000000000000000000000000000000000000000000000000
        redBoard = 0b0000000000000000000000000000000000000000000000000000000000000000

        #   Create temporary random boards for time testing
        #   Create green board
        for piece in range(8):
            bitShift = random.randint(0, 63)
            if ~(allBoard & (1 << bitShift)):
                allBoard |= (1 << bitShift)
                greenBoard |= (1 << bitShift)
        #   Create red board
        for piece in range(8):
            bitShift = random.randint(0, 63)
            if ~(allBoard & (1 << bitShift)):
                allBoard |= (1 << bitShift)
                redBoard |= (1 << bitShift)

        for time in range(0, 120, 5):
            plys = self.findNextMove(time, 1, allBoard, greenBoard, redBoard)
            #print(plys)
            print(time, ": ", len(plys[0]))
            plysVSTime[time / 5] = len(plys[0])
        print(plysVSTime)


halma = Halma([[1, 1], [2, 2]], 8)
halma.analyzeMinimax()
#halma.play(5)

#   TODO    INTEGRATE THE UTILITY FUNCTION INTO MIN AND MAX
#   TODO    add analytics into minimax
#   TODO    make the UI update with the time remaining
#   TODO    once someone wins, display the number of moves made and teh final score
#               the score is +1 for each piece in the camp + 1/d for each piece outside where d = shortest distance from
#                   the piece to the base
