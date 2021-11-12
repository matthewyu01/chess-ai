import threading
import berserk
import chess
with open('.env') as f:
    token = f.read()
session = berserk.TokenSession(token)
client = berserk.Client(session)

import torch
import torch.nn as nn
import torch.nn.functional as F
from generate_data import *
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(385, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32,8)
        self.fc4 = nn.Linear(8, 1)
    def forward(self, x):
        x = self.fc1(x)
        x = torch.reshape(x, (-1,)) # flattens into 1d tensor                                                      
        x = self.fc2(x)
        x = self.fc3(F.relu(x))
        x = self.fc4(torch.sigmoid(x))
        return x
net = Net()
net.load_state_dict(torch.load('Models/chess_ai1.1.pt'))
net.eval()
def nn_prediction(position: chess.Board):
    board_rep = convert_board(position)
    torch_board = torch.from_numpy(board_rep.reshape(1, 385)).float()
    return net(torch_board)
def minimax(position, depth, maximizingPlayer, alpha = -1e9, beta = 1e9):
            
    if position.is_checkmate():
        if maximizingPlayer:
            alpha = 1e3
            return 1e3
            
        else:
            beta = -1e3
            return -1e3
         #pick move if its checkmate
                                                              
    if depth == 0 or position.is_game_over():
        return nn_prediction(position)
    
    if maximizingPlayer:
        value = -1e9
        for move in position.legal_moves:
            position.push(move)
            value = max(value, minimax(position, depth-1, False, alpha, beta))
            position.pop()
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = 1e9
        for move in position.legal_moves:
            position.push(move)
            value = min(value, minimax(position, depth-1, True, alpha, beta))
            position.pop()
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def find_best_move(position, depth):
    best_evaluation = -1e9
    for move in position.legal_moves:
        position.push(move)
        if position.is_checkmate(): #pick move if its checkmate
            return move
        nn_eval = minimax(position, depth - 1, False, -1e9, 1e9)
        position.pop()
        if nn_eval > best_evaluation:
            best_evaluation = nn_eval
            best_move = move
    try:
        return best_move
    except:
        return None

class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
        game_state = self.current_state['state']
        self.my_color = "WHITE" if client.account.get()['id'] == self.current_state["white"]["id"] else "BLACK"
        if self.my_move(game_state["moves"]):
            self.handle_state_change(game_state)
    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                print(event)
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)
    def get_move(self, board):
        nn_move = find_best_move(board,3)

        return str(nn_move)
        # return random.choice(list(board.legal_moves)).uci() # random move                                        
    def handle_state_change(self,game_state):
        board = chess.Board()
        #play moves on new chess board                                                                             
        moves = [] if game_state["moves"] == "" else game_state["moves"].split(" ")
        for move in moves:
            board.push_uci(move)
        move = self.get_move(board)
        if move == 'None':
            return
        print(type(move))
        status = game_state['status']
        try:
            if self.my_move(game_state["moves"]) and status == "created" or status == "started":
                print(move, self.game_id)
                self.client.bots.make_move(self.game_id, move)
        except:
            pass
            #error                                                                                                 
     #   self.moved = True      
    def my_move(self, moves):
        valid_move_list = [] if moves == "" else moves.split(" ")
        num_moves = len(valid_move_list)
        board_move = "WHITE" if num_moves % 2 == 0 else "BLACK"
        print(board_move)
        return self.my_color == board_move
    def handle_chat_line(self, chat_line):
        pass
    is_polite = True
while True:
    for event in client.bots.stream_incoming_events():
        if event['type'] == 'challenge':
            client.bots.accept_challenge(event['challenge']['id'])
        elif event['type'] == 'gameStart':
            game = Game(client, event['game']['id'])
            game.start()
     