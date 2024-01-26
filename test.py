from player import AI, Computer
from game import Game

board = [ 
    [ 'o', 'x', 'o' ],  
    [ 'x', 'x', 'o' ],  
    [ ' ', ' ', ' ' ]  
] 

player1= Computer('e')
player2=AI('h')
t=Game(player1, player2)
t.board= board
bestMove = player2.get_moves(t)  
  
print("The Optimal Move is :")  
print("ROW:", bestMove[0], " COL:", bestMove[1]) 