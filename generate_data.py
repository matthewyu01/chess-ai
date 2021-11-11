import chess
import chess.engine
import numpy as np
import pandas as pd
import random

# https://python-chess.readthedocs.io/en/latest/
# https://python-chess.readthedocs.io/en/latest/core.html

STOCKFISH = chess.engine.SimpleEngine.popen_uci("Engines/stockfish_13_win_x64_bmi2")
ALL_SQUARES = chess.SquareSet(chess.BB_ALL)


def stockfish_evaluation(board, depth=2):
    info = STOCKFISH.analyse(board, chess.engine.Limit(depth=depth))
    board_eval = info['score'].white().score(mate_score=2000)
    return board_eval


def generate_rand_board():
    board = chess.Board()
    #moves = random.randint(1,80) #1-80 moves. don't want to confuse NN with endgame
    moves = random.randint(1,20) # focus on opening

    for _ in range(moves):
        potential_moves = list(board.legal_moves)
        chosen_move = random.choice(potential_moves)
        old_board = board.copy()
        board.push(chosen_move)
        if board.is_game_over():
            return old_board

    return board


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



def get_data():
    data_list = []

    for _ in range(30000):
        board = generate_rand_board()
        eval_ = stockfish_evaluation(board)

        x = np.append(convert_board(board), [eval_]) 
        data_list.append(x)

    df = pd.DataFrame(data_list)

    stockfish_data = df.to_csv('Data/stockfish_depth0_opening10.csv', index = False, header = False) 


def best_moves(depth = 20):
    data_list = []

    board = chess.Board()
    moves = random.randint(1,depth) 

    for _ in range(moves):
        potential_moves = list(board.legal_moves)
        chosen_move = random.choice(potential_moves)
        old_board = board.copy()
        board.push(chosen_move)
        if board.is_game_over():
            return old_board


    df = pd.DataFrame(data_list)

    stockfish_data = df.to_csv('Data/stockfish_depth0_9.csv', index = False, header = False) 

if __name__ == "__main__":
    get_data()
    print('DONE')