"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xcount = 0
    ocount = 0
    for i in board:
        for j in i:
            if j == X:
                xcount+=1
            if j == O:
                ocount+=1
    
    if ocount < xcount:
        return O
    else:
        return X




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.append((i,j))
    
    return possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    temp = list(board)
    temp[i][j] = player(board)
    return temp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #checking horizontal
    for i in board:
        if i[0] == i[2] and i[1] == i[2]:
            return i[0]
    #checking columns
    for i in range(3):
        if board[0][i] == board[1][i] and board[0][i] == board[2][i]:
            return board[0][i]
    #check diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def score(move,board):
    new_board = result(board,move)
    if terminal(new_board):
        return utility(new_board)
    
    current = player(new_board)
    if current == X:
        desired = 1
    else:
        desired = -1
    
    possible_actions = list(actions(new_board))
    for i in range(len(possible_actions)):
        possible_actions[i] = (possible_actions[i],score(possible_actions[i],board))
    for i in possible_actions:
        if i[1] == desired:
            return i[1]
    for i in possible_actions:
        if i[1] == 0:
            return 0
    return possible_actions[0][1]

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current = player(board)
    if current == X:
        desired = 1
    else:
        desired = -1
    
    moves = list(actions(board))
    values = []
    for i in moves:
        values.append(score(i,board))
    moves = tuple(zip(moves,values))
    for i in moves:
        if i[1] == desired:
            return i[0]
    for i in moves:
        if i[1] == 0:
            return i[0]
    return moves[0][0]

