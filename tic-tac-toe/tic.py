#!/usr/bin/env python2.7

'''
TTTBoard Class Information
'''

# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        self._dim = dim
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(dim)]
                           for dummyrow in range(dim)]
        else:
            # Copy board grid
            self._board = [[board[row][col] for col in range(dim)]
                           for row in range(dim)]

    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim

    def square(self, row, col):
        """
        Return the status (EMPTY, PLAYERX, PLAYERO) of the square at
        position (row, col).
        """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        Does nothing if board square is not empty.
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """
        If someone has won, return player.
        If game is a draw, return DRAW.
        If game is in progress, return None.
        """
        lines = []

        # rows
        lines.extend(self._board)

        # cols
        cols = [[self._board[rowidx][colidx] for rowidx in range(self._dim)]
                for colidx in range(self._dim)]
        lines.extend(cols)

        # diags
        diag1 = [self._board[idx][idx] for idx in range(self._dim)]
        diag2 = [self._board[idx][self._dim - idx -1]
                 for idx in range(self._dim)]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None

    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board)


def switch_player(player):
    """
    Convenience function to switch players.

    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX

def play_game(mc_move_function, ntrials, reverse = False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None

    # Run game
    while winner == None:
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = switch_player(curplayer)

        # Display board
        print board
        print

    # Print winner
    if winner == PLAYERX:
        print "X wins!"
    elif winner == PLAYERO:
        print "O wins!"
    elif winner == DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random


# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 99         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

def create_initial_score(dim):
    """
    function to create a empty score grid
    """
    init_scores=[[0 for _row in range(dim)]
                    for _col in range(dim)]
                
    return init_scores

# Add your functions here.
def mc_trial(board, player):
    """
     This function takes a current board and the next player to move.
     The function should play a game starting with the given player
     by making random moves, alternating between players.
     The function should return when the game is over.
     The modified board will contain the state of the game,
     so the function does not return anything.
     In other words, the function should modify the board input.
    """
    tmp_player=player
    while board.check_win()==None:
        #print board.check_win()
        empty=board.get_empty_squares()
        #print empty
        square=random.choice(empty)
        #print square
        board.move(square[0],square[1],tmp_player)
        tmp_player=switch_player(tmp_player)
    return

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same
    dimensions as the Tic-Tac-Toe board, a board from a completed game,
    and which player the machine player is. The function should score
    the completed board and update the scores grid. As the function
    updates the scores grid directly, it does not return anything,
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.check_win()==player:
                if board.square(row,col)==player:
                    scores[row][col]+=SCORE_CURRENT
                elif board.square(row,col)==switch_player(player):
                    scores[row][col]-=SCORE_OTHER
            elif board.check_win()==switch_player(player):
                if board.square(row,col)==player:
                    scores[row][col]-=SCORE_CURRENT
                elif board.square(row,col)==switch_player(player):
                    scores[row][col]+=SCORE_OTHER
    return

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    The function should find all of the empty squares with the maximum
    score and randomly return one of them as a (row, column) tuple.
    It is an error to call this function with a board that has no empty
    squares (there is no possible next move), so your function may do
    whatever it wants in that case. The case where the board is full will
    not be tested.
    """
    if board.check_win()==None:
        maximum=-999
        ret_location=(0,0)
        empty=board.get_empty_squares()
        #print empty
        for position in empty:
            if scores[position[0]][position[1]]>maximum:
                maximum=scores[position[0]][position[1]]
                #print max
                ret_location=(position[0],position[1])
        return ret_location
    else:
        return None

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is,
    and the number of trials to run. The function should use the Monte Carlo
    simulation described above to return a move for the machine player
    in the form of a (row, column) tuple.
    """
    scores = create_initial_score(board.get_dim())
    for _ in range(trials):
        board1=board.clone()
        mc_trial(board1,player)
        mc_update_scores(scores, board1, player)
    return get_best_move(board, scores)

play_game(mc_move, NTRIALS, False)


