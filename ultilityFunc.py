import math


#   @brief  A more subtle version of the isWin function from phase 1
#           that scores how good a board is.
#
#   @details It adds up the distance each piece is from being in the
#            goal camp (lower scores best; shortest distance from
#            goal camp).
#
#   @param[out] string
#               Returns a string that states whether the board is good
#               for either opponent.
def util_funct(self, all_board, color_board, board_pos):
    score = 0.0

    # Checks how far green has to enemy camp
    if color_board == "green" & (1<< board_pos):

        # For each green piece
        for x in range(self.dimen):
            for y in range(self.dimen):

                # Get the closest row to each piece based on where they are on the board
                row_x = find_closest_row(self, x, all_board)

                # Get the closest column to each piece based on where they are on the board
                col_y = find_closest_col(self, y, all_board)

                # Calculate the distance to the nearest space in the enemy camp
                dis = calculate_distance(x, row_x, y, col_y)

                # Add it to the score based on whether the piece is in the enemy camp
                if dis == 0:
                    score += 1
                else:
                    score += (1/dis)

    # For each red piece not in the enemy camp
    else:
        for x in range(self.dimen/2,self.dimen):
            for y in range(self.dimen/2,self.dimen):
                # Get the closest row to each piece based on where they are on the board
                row_x = find_closest_row(self, x, all_board)

                # Get the closest column to each piece based on where they are on the board
                col_y = find_closest_col(self, y, all_board)

                # Calculate the distance to the nearest space in the enemy camp
                dis = calculate_distance(x, row_x, y, col_y)

                # Add it to the score
                if dis == 0:
                    score += 1
                else:
                    score += (1/dis)

    # Return the score
    return score

"""
    @brief         Gets the closest row to the given piece
    
    @param[in]     curr_row
                   The current row that that given piece is in
    
    @param[out]    int
                   an integer representing the closest row
"""


def find_closest_row(self, curr_row, board):

    # for green pieces, if the corner is unoccupied by a green piece, use the row 0
    # else
    if self.GreenBoard:
        if (curr_row - 3) > 0:
            close_row = curr_row
        else:
            close_row = 0
    else:
        if (curr_row - 4) > 0:
            close_row = curr_row
        else:
            close_row = 7

    return close_row


"""
    @brief         Gets the closest column to the given piece

    @param[in]     curr_col
                   The current column that that given piece is in

    @param[out]    int
                   an integer representing the closest column
"""


def find_closest_col(self, curr_col, board):

    # for green pieces, if the piece is not in the base, then set column to
    # 0; otherwise, set the closest column to the current column
    if self.greenBoard:
        if (curr_col - 3) > 0:
            close_col = curr_col
        else:
            close_col = 0

    else:
        if (curr_col - 4) > 0:
            close_col = curr_col
        else:
            close_col = 7

    return close_col


"""
    @brief          Calculates the distance between the current location
                    and the closest location in the enemy camp
    
    @param[in]      row1
                    the current row number of the piece/smallest value
    
    @ param[in]     row2
                    the closest row to the piece/largest value
    
    @param[in]      col1
                    the current column number of the piece/smallest value
    
    @ param[in]     col2
                    the closest column to the piece/largest value                
    
    @param[out]     double
                    a number that is the distance between the two locations
"""


def calculate_distance(row1, row2, col1, col2):

    row_val = math.pow((row2 - row1), 2)

    col_val = math.pow((col2 - col1), 2)

    distance = math.sqrt((row_val + col_val))

    return distance
