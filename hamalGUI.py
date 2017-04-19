import tkinter
from tkinter import ttk

# puts up board window
def init_gui(self, board):
    self.root.title('Welcome to Halma')

    draw_board(board)


# draws the board with buttons
def draw_board(board):
    hButton = ttk.Button()
    for r in len(board):
        for c in len(board):

    return

# place pieces on board
def place_pieces(board):
    r = 1
    while r < 5:
        r += 1

    r = len(board)
    while r > 4:
        r -= 1
    return

# place green piece in new location on board
def place_green_piece(board):
    return

# place red piece in new location on board
def place_red_piece(board):

        return


# updates board when a move is made
def update_board(board):

