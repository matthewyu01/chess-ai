import pygame

import pieces



board = [['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R','N','B','Q','K','B','N','R'],]


class Board:
    def __init__(self, board, white_move = True) -> None:
        self.board = board
        self.pieces = []
        self._white_move = white_move
        
    def update(self):
        pass

    def is_whites_move(self):
        return self._white_move

        
    def add_piece(self, piece):
        row = piece.row
        col = piece.col
        if board[row][col] != '':
            #raise PieceOverlapError
            return
        else:
            board[row][col] = piece.letter

a = Board(board)

BOARD_WIDTH = 480
BOARD_HEIGHT = 480

