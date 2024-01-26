
import pygame as pg
import time
import sys
from pygame.locals import *
from player import Human, Computer, AI
pg.init()

width = 400
height = 400
line_color = (0, 0, 0)
line_width= 5
cell_size = width //3
fps = 30
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)

pg.display.set_caption("Tic Tac Toe")
#loading the image for 'x' and 'o'
x_letter = pg.image.load("x.png")
o_letter = pg.image.load("o.png")

#resizing the images to fit the screen
x_letter = pg.transform.scale(x_letter, (80, 80))
o_letter = pg.transform.scale(o_letter, (80, 80))

class Game:
    #initializing game class
    #board is in format of rows and column: 
    #   1  2   3
    #1 []  []  []
    #2 []  []  []
    #3 []  []  []
    def __init__(self, player1, player2):
        self.board = [[' ']*3, [' ']*3, [' ']*3]
        self.draw = False
        self.winner = None
        self.current_player = 'x'
        self.player1 = player1
        self.player2 = player2
       
    def check_win(self, draw):
            #check wins for rows
            for row in range(0, 3):
                if((self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board[row][0] != ' ')):
                    self.winner = self.board[row][0]
                    if draw:
                        pg.draw.line(screen, (250, 0, 0),
                                    (0, (row + 1)*height / 3 - height / 6),
                                    (width, (row + 1)*height / 3 - height / 6),
                                    4)
                    

            # check wins for columns
            for col in range(0, 3):
                if((self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] !=  ' ')):
                    self.winner = self.board[0][col]
                    if draw:
                        pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                                    ((col + 1) * width / 3 - width / 6, height), 4)
                    

            # check for diagonal wins
            if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] !=  ' '):
                # game won diagonally left to right
                self.winner = self.board[0][0]
                if draw:
                    pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
                

            if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] !=  ' '):
                # game won diagonally right to left
                self.winner = self.board[0][2]
                if draw:
                    pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
                

            #check for draws
            if(self.get_empty_slots() == [] and self.winner == None):
                self.draw = True

   
    #displays the 'x' or 'o' onto the grid based on user clicks or computer
    def draw_letter(self, row, col):
        #convert row into x coordinates
        if row == 1:
            pos_x = 30
        elif row == 2:
            pos_x = width // 3 + 30
        elif row == 3:
            pos_x = width // 3 * 2 + 30

        #convert col into x coordinates
        if col == 1:
            pos_y = 30
        elif col == 2:
            pos_y = height // 3 + 30
        elif col == 3:
            pos_y = height // 3 * 2 + 30

        #mark the col and row with current player
        self.board[row-1][col-1] = self.current_player
    
        if self.current_player == 'x':
            screen.blit(x_letter, (pos_y, pos_x))
            self.current_player = 'o'
        else:
            screen.blit(o_letter, (pos_y, pos_x))
            self.current_player = 'x'

        #checks current state of the board
        self.check_win(True)
        #displays appropriate message depending on current state of the board
        if self.draw:
            message = "It's a draw!"
        elif self.winner is None:
            message = self.current_player + "'s Turn"
        else:
            message = self.winner + " player won!"
        
        font = pg.font.Font(None, 30)
        text = font.render(message, 1, (255, 255, 255))
        screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(width / 2, 500-50))
        screen.blit(text, text_rect)
        pg.display.update()


    def user_click(self):
        #gets the coordinates of where the user clicked on the grid and converts it into row and col on the board
        x, y = pg.mouse.get_pos()

        if (x < width /3):
            col = 1
        elif(x < width / 3 * 2):
            col = 2
        elif (x < width):
            col  = 3
        
        if (y < height /3):
            row = 1
        elif(y < height / 3 * 2):
            row = 2
        elif (y < height):
            row = 3

        #checks if row and col is empty
        if(row and col and self.board[row-1][col-1] == ' '):
            self.draw_letter(row, col)
            
        
        pg.display.update()
            
 
    def get_empty_slots(self):
        #goes through the board and returns all the unmarked slots
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def undo_moves(self, row, col):
        self.board[row][col] = ' '
    


def draw_board():
    for i in range(1,3):
        pg.draw.line(screen, line_color, (0, i * cell_size), (width, i * cell_size), line_width)
        pg.draw.line(screen, line_color, (i * cell_size,0), (i * cell_size, height), line_width)

def reset_game(game):
    game.winner = None
    game.draw = False
    game.board = [[' ']*3, [' ']*3, [' ']*3]
    game.current_player= 'x'
    time.sleep(3)
    screen.fill([255, 255, 255])
    draw_board()


def game_play(game, running=True):
    pg.display.update()
    time.sleep(3)
    screen.fill([255, 255, 255])
    draw_board()
    
    while running:
        for event in pg.event.get():
            #stops the game if the user click on the close button
            if event.type == pg.QUIT:
                running = False
            #if user clicked on the board, the coordinates get recorded to mark the area
            elif event.type == MOUSEBUTTONDOWN:
                game.user_click()
                #checks state of board 
                if game.winner or game.draw:
                    running = False
                    
        #calls non human player
        if game.current_player == 'o' and not game.winner and not game.draw:
            if game.player2 != 'h':
                pg.display.update()
                #gets the computer's next moves
                move = game.player2.get_moves(game)
                
                #checks validity of move
                if move is not None:
                    row, col = move
                    pg.time.wait(1000)
                    #display chosen spot
                    game.draw_letter(row + 1, col + 1)
                    if game.winner or game.draw:
                        running = False

        pg.display.update()
        clock.tick(fps)

    
class Menu:
    def __init__(self):
        self.font = pg.font.Font(None, 36)
        self.options = ["Human", "Computer(EASY)", "Computer(HARD)", "Quit"]
        self.selected_option = None

    #displays the menu option 
    def draw(self):
        screen.fill((255, 255, 255))
         
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            rect = text.get_rect(center=(width // 2, height // 2 + i * 40))
            screen.blit(text, rect)

    
    def handle_click(self, x, y):
        for i, option in enumerate(self.options):
            rect = pg.Rect((width // 2 - 50, height // 2 + i * 40 - 20, 100, 40))
            if rect.collidepoint(x, y):
                self.selected_option = option
                return True
        return False

def main_menu():
    menu = Menu()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if menu.handle_click(x, y):
                    running = False

        menu.draw()
        pg.display.flip()
        clock.tick(fps)

    return menu.selected_option

def main():
    running = True

    while running:
        selected_option = main_menu()

        player1 = Human('h')

        if selected_option == "Human":
            player2 = Human('h')
        elif selected_option == "Computer(EASY)":
            player2 = Computer('e')
        elif selected_option == "Computer(HARD)":
            player2 = AI('ai')
        elif selected_option == "Quit":
            running = False
            sys.exit()
        else:
            # Default to Human player if an invalid option is selected
            player2 = Human('h')
        
        game = Game(player1, player2)
        game_play(game,True)
        reset_game(game)


if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()