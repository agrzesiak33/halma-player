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
        notification = Label(self.notificationFrame, textvariable=var)
        var.set("Hello welcome to Halma")
        notification.pack()
        self.notificationFrame.grid(row=0)

        #   Initialize the board to the dimensions specified
        self.boardFrame.grid(row=1)
        self.boardFrame.config(bg='black')
        for row in range(1, self.dimen + 1):
            for column in range(self.dimen):

                #   Create all the buttons for the board
                button = Button(self.boardFrame)
                button.grid(row=row, column=column)
                button.text = "empty"   #The text field is how we will keep track of the status of each button
                button.config(image=self.empty, width="100", height="100")
                button.bind("<Button-1>", self.handleClick)

        self.root.mainloop()

    def handleClick(self, event):
        if event.widget.text == "empty":
            print("It's empty")
            event.widget.image = self.dark_green
            event.widget.text = "real green"
            event.widget.config(image = self.dark_green)
        elif event.widget.text == "real green":
            print("There is an actual green tile here")
            event.widget.image = self.light_green
            event.widget.text = "virtual green"
            event.widget.config(image=self.light_green)
        elif event.eidget.text == "virtual green":
            print("There used to be a green piece here")
            event.widget.image = self.light_green
            event.widget.text = "virtual green"
            event.widget.config(image=self.light_green)
        elif event.widget.text == "real red":
            print("there is an actual red tile here")
        elif event.widget.text == "virtual red":
            print("There used to be a red piece here")


board = Board(10)