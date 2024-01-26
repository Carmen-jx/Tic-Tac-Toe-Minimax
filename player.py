import math
import random
import copy

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_moves(self, game):
        pass

class Human (Player):            
    def __init__(self,letter):
        super().__init__(letter)

    def get_moves(self, game):
        pass

class Computer (Player):
    def __init__(self,letter):
        super().__init__(letter)
        
    def get_moves(self, game):
        square = random.choice(game.get_empty_slots())
        if square:
            return square
        return None

class AI (Player):
    def __init__(self,letter):
        super().__init__(letter)

    def get_moves(self, game):
        #calls minimax function to get the optimal move
        move_val,best_move = self.minimax(game, 0, False)
        game.winner = None
        game.draw = False
       
        return best_move
    
    def minimax(self, game, depth, max_playing):
        #check state og board
        game.check_win(False)

        if game.winner =='x':    
            return 1, None
        elif game.draw:
            return 0, None
        elif game.winner == 'o':
            return -1, None
           
        #assume that player 'x' (human player) plays the most optimal moves
 
        if max_playing:
            best = -math.inf
            avail_moves = game.get_empty_slots()

            for (row,col) in avail_moves:
                game.board[row][col] = 'x'
                #recursive call to determine best move_val and best move
                move_val = self.minimax(game, depth +1, False)[0]
                #checks if move is optimal depending on the move_values
                if move_val> best:
                    best= move_val
                    best_move= (row,col)
                game.undo_moves(row, col)
                game.winner = None
                game.draw = False

           # print("depth:", depth, "best:", best)
            return best, best_move  
        
        else:
            best= math.inf
            avail_moves = game.get_empty_slots()

            for (row,col) in avail_moves:
                game.board[row][col] = 'o'
                #recursive call to determine best move_val and best move
                move_val = self.minimax(game, depth + 1,  True)[0]
                #checks if move is optimal depending on the move_values
                if move_val < best:
                    best = move_val
                    best_move = (row,col)
                game.undo_moves(row, col)
                game.winner = None
                game.draw = False

            return best, best_move
        


  

        