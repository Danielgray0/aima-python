from collections import namedtuple
from games import (Game)

class GameState:
    def __init__(self, to_move, board, label=None, depth=8):
        self.to_move = to_move
        self.board = board
        self.label = label
        self.maxDepth = depth

    def __str__(self):
        if self.label == None:
            return super(GameState, self).__str__()
        return self.label

class FlagrantCopy(Game):
    """A flagrant copy of TicTacToe, from game.py
    It's simplified, so that moves and utility are calculated as needed
    Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=6, v=7, k=4):
        self.h = h
        self.v = v
        self.k = k
        self.initial = GameState(to_move='X', board={})

    def actions(self, state):
        try:
            return state.moves
        except:
            pass
        "Legal moves are any square not yet taken, at the lowest available spot in each column."
        moves = []
        for y in range(1, self.v + 1):
            for x in range(self.h , 0, -1):
                if (x,y) not in state.board.keys():
                    moves.append((x,y))
                    break
        state.moves = moves
        return moves

    # defines the order of play
    def opponent(self, player):
        if player == 'X':
            return 'O'
        if player == 'O':
            return 'X'
        return None

    def result(self, state, move):
        if move not in self.actions(state):
            return state  # Illegal move has no effect
        board = state.board.copy()
        player = state.to_move
        board[move] = player
        next_mover = self.opponent(player)
        return GameState(to_move=next_mover, board=board)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        try:
            return state.utility if player == 'X' else -state.utility
        except:
            pass
        board = state.board
        util = self.check_win(board, 'X')
        if util == 0:
            util = -self.check_win(board, 'O')
        state.utility = util
        return util if player == 'X' else -util

    # Did I win?
    def check_win(self, board, player):
        # check rows
        for x in range(1, self.h - 2):
            for y in range(1, self.v + 1):
                if self.k_in_row(board, (x,y), player, (1,0)):
                    return 1
        # check columns
        for y in range(1, self.v - 2):
            for x in range(1, self.h + 1):
                if self.k_in_row(board, (x,y), player, (0,1)):
                    return 1
        # check \ diagonal
        for x in range(1, self.h - 2):
            for y in range(1, self.v - 2):
                if self.k_in_row(board, (x,y), player, (1,1)):
                    return 1
        # check / diagonal
        for x in range(self.h , 3, -1):
            for y in range(1, self.v - 2):
                if self.k_in_row(board, (x,y), player, (-1,1)):
                    return 1
        return 0

    # does player have K in a row? return 1 if so, 0 if not
    def k_in_row(self, board, start, player, direction):
        "Return true if there is a line through start on board for player."
        (delta_x, delta_y) = direction
        x, y = start
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = start
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted start itself twice
        return n >= self.k

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return self.utility(state, 'X') != 0 or len(self.actions(state)) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()


myGame = FlagrantCopy()

testState = GameState(
    to_move = 'O',
    board = {
             (4,1): 'O', (4,2): 'O', (4,3): 'X', (4,4): 'O', (4,5): 'O', (4,6): 'O', (4,7): 'X',
             (5,1): 'O', (5,2): 'X', (5,3): 'O', (5,4): 'X', (5,5): 'X', (5,6): 'X', (5,7): 'O',
             (6,1): 'X', (6,2): 'X', (6,3): 'O', (6,4): 'X', (6,5): 'O', (6,6): 'X', (6,7): 'X',
            },
    label = 'AB(2)>AB(0)'
)

winin1 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O',
            },
    label = 'winin1'
)

losein1 = GameState(
    to_move = 'O',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O',
             (3,1): 'X',
            },
    label = 'losein1'
)

winin3 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'O',
             (2,1): 'X',
             (3,1): 'O',
            },
    label = 'winin3'
)

losein3 = GameState(
    to_move = 'O',
    board = {(1,1): 'X',
             (2,1): 'X',
             (3,1): 'O', (1,2): 'X', (1,2): 'O',
            },
    label = 'losein3'
)

winin5 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'O',
             (2,1): 'X',
            },
    label = 'winin5'
)

lost = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O', (2,3): 'O',
             (3,1): 'X'
            },
    label = 'lost'
)

myGames = {
    myGame: [
        testState
        # winin1, losein1, winin3, losein3, winin5,
        # lost,
    ]
}