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

        self.tester()
        self.root.mainloop()

    def handleClick(self, event):
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

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



    def tester(self):
        self.listBoard[4][0].image = self.dark_green
        self.listBoard[4][0].bind("<Button-1>", self.handlePieceClick)
        self.listBoard[4][0].config(image = self.dark_green)
        self.listBoard[4][1]="green"

        self.listBoard[5][0].image = self.dark_green
        self.listBoard[5][0].bind("<Button-1>", self.handlePieceClick)
        self.listBoard[5][0].config(image=self.dark_green)
        self.listBoard[5][1] = "green"

        self.listBoard[1][0].image = self.dark_red
        self.listBoard[1][0].bind("<Button-1>", self.handlePieceClick)
        self.listBoard[1][0].config(image=self.dark_red)
        self.listBoard[1][1] = "red"

        self.listBoard[2][0].image = self.dark_red
        self.listBoard[2][0].bind("<Button-1>", self.handlePieceClick)
        self.listBoard[2][0].config(image=self.dark_red)
        self.listBoard[2][1] = "red"

    def handlePieceClick(self, event):
        print("Handling", self.turn, "click")
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        #   If it is greens turn and the space just clicked is green
        if self.listBoard[x * self.dimen + y][1] is self.turn and self.buttonJustClicked is None:
            self.listBoard[x * self.dimen + y][1] = "selected"
            self.listBoard[x * self.dimen + y][0].config(bg = 'blue')
            self.buttonJustClicked = self.listBoard[x * self.dimen + y][0]
            print("Selected a ",self.turn," piece")
        #   If there already was a selection and we need to move into the new spot
        elif self.buttonJustClicked is not None:
            oldXY = self.buttonJustClicked.text.split(",")
            oldX = int(oldXY[0])
            oldY = int(oldXY[1])
            if self.listBoard[x *self.dimen + y][1] is not "empty":
                print("There is already a piece there")
                #   Unselecting the button
                self.listBoard[oldX * self.dimen + oldY][0].config(bg = 'white')
                self.listBoard[oldX * self.dimen + oldY][1] = self.turn
                self.buttonJustClicked = None
            else:
                print("handling making teh selection")
                #   Getting rid of old tile
                self.listBoard[oldX * self.dimen + oldY][1] = "empty"
                self.listBoard[oldX * self.dimen + oldY][0].image = self.empty
                self.listBoard[oldX * self.dimen + oldY][0].config(image = self.empty, bg = 'white')
                self.listBoard[oldX * self.dimen + oldY][0].bind("<Button-1>", self.handleClick)

                #   Changind the new square to the green tile
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
                    if self.isInBounds(newX, newY) and self.listBoard[newX * self.dimen + newY][1] is "empty":
                        legalMoves.append([newX, newY])
                        self.findJumps(visited, legalMoves, newX, newY)


    def isInBounds(self, x,y):
        if x<0 or x>= self.dimen or y<0 or y >=self.dimen:
            return False
        else:
            return True
board = Board(10)