class Piece:
    def __init__(self, board, square, white):
        self.square = square
        self.row = square[0]
        self.col = square[1]
        self.is_clicked = False #dk if i need this
        self._white = white
        self.pinned = False
        #self.letter

    def move(self):
        pass

    def check_move(self):
        if self.is_clicked == True:
            pass
        
    def clicked(self):
        self.is_clicked = True

    #white is uppercase

    #black loewrcase
    

    #team

class Not_King(Piece):
    def __init__(self, square, white):

        #super().__init__(self, fname, lname)
        super().__init__(square, white)
        self.square = square
        self.is_pinned = False
        self.is_protected = False
    
    def check_pinned(self):
        pass
    def check_protection(self):
        pass
class King(Piece):
    def move(self):
        moves = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),]
        pass
        #check squares


class Knight(Not_King):
    def move(self):
        moves = [(-1, -2), (-1, 2), (1, 2), (1,-2), 
            (-2, -1), (-2, 1), (2, -1), (2, 1)]
    #move
    #check L shape 2,1
    pass
class Pawn(Not_King):
    def move(self):
        pass
        # check squares of board
    def __init__(self, board, square, white):
        super().__init__(board, square, white)
        if self._white:
            self.moves = [(-1,0)] #-1 row is going up one row
        else:
            self.moves = [(1,0)]
        
    
    def move(self):
        pass


    def possible_moves(self):
        if self._white: #white
            #board
            pass
        else: #black 
            pass
        #
