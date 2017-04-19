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
                self.handleGreenClick(event)
            else:
                print("illegal move")
                self.listBoard[oldx * self.dimen + oldy][1] = "green"
                self.buttonJustClicked = None



        #self.handleGreenClick(event)
        print(event.widget.text)



    def tester(self):
        self.listBoard[4][0].image = self.dark_green
        self.listBoard[4][0].bind("<Button-1>", self.handleGreenClick)
        self.listBoard[4][0].config(image = self.dark_green)
        self.listBoard[4][1]="green"

    def handleGreenClick(self, event):
        print("Handling green click")
        xy = event.widget.text.split(",")
        x = int(xy[0])
        y = int(xy[1])

        if self.turn is "green" and self.listBoard[x * self.dimen + y][1] is "green":
            self.listBoard[x * self.dimen + y][1] = "selected"
            self.buttonJustClicked = self.listBoard[x * self.dimen + y][0]
            print("Selected a green piece")
        elif self.turn is "green" and self.buttonJustClicked is not None:
            print("handling making teh selection")
            oldXY = self.buttonJustClicked.text.split(",")
            self.listBoard[int(oldXY[0]) * self.dimen + int(oldXY[1])][1] = "empty"
            self.buttonJustClicked.image = self.empty
            self.buttonJustClicked.config(image = self.empty)
            self.buttonJustClicked.unbind("<Button-1>")

            event.widget.image = self.dark_green
            event.widget.config(image = self.dark_green)
            self.listBoard[x*self.dimen + y][0].bind("<Button-1>", self.handleGreenClick)
            self.listBoard[x * self.dimen + y][1] = "green"
            self.buttonJustClicked = None

    def generateLegalMoves(self, x, y):
        legalMoves = []

        #   Find if the places around it are open
        for row in range(x-1, x+2):
            if row >= 0 and row < self.dimen:
                for column in range(y-1, y+2):
                    if column >= 0 and column < self.dimen:
                        if self.listBoard[row * self.dimen + column][1] == "empty":
                            legalMoves.append([row, column])
        return legalMoves

board = Board(10)