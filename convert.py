import chess
import numpy as np

# https://python-chess.readthedocs.io/en/latest/
# https://python-chess.readthedocs.io/en/latest/core.html

ALL_SQUARES = chess.SquareSet(chess.BB_ALL)

def convert_sqr(sqr):
    """
    Converts index (0,63) to 2d indices of (0,7)
    """
    #r = 7 - r   #7-r flips rows so array looks like chess board
    return 7 - (sqr // 8), sqr % 8 

def convert_board(board):
    """
    Converts board to matrix representation
    """
    #init matrix
    board_rep = np.zeros((6, 8, 8)) 
    
    #get all pieces in position
    for piece in chess.PIECE_TYPES: #piece is an int [1,6]
        for sqr in board.pieces(piece, chess.WHITE): #sqr is an int [0,63]
            r, c = convert_sqr(sqr)
            board_rep[piece-1][r][c] = 1
        for sqr in board.pieces(piece, chess.BLACK): 
            r, c = convert_sqr(sqr)
            board_rep[piece-1][r][c] = -1

    if board.turn == chess.WHITE:
        board_rep2 = np.append(board_rep.reshape(-1), [3])
    else:
        board_rep2 = np.append(board_rep.reshape(-1), [-3])
    return board_rep2