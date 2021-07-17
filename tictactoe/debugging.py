import tictactoe as t
EMPTY = None
X = 'X'
O = 'O'
board = [[X, X, O],[X, O, X],[O, O, X]]
print(t.player(board))
print(t.minimax(board))



