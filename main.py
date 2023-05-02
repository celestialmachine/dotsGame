#Programmer: Victor Diaz
#I state the code submitted is my own

from typing_extensions import Self
import pygame
import board
import UI
from sys import exit

#Game constants
TILE_SIZE = 60
BOARD_TILE_WIDTH = 8
BOARD_TILE_HEIGHT = 6  
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
FPS = 60
DOT_SIZE = 8
LINE_WIDTH = 8

class Game(object):
    #game constructor
    def __init__(self) -> None:
        self.playerOneScore = 0
        self.playerTwoScore = 0
        self.scoreToWin = self.points_to_win()
        self.dotBoard = board.DotBoard()
        #Bool means two players only
        self.playerOneTurn = True
    
    #calculate points needed to win: < half of available squares
    def points_to_win(self):
        maxPoints = 0
        if (BOARD_TILE_WIDTH * BOARD_TILE_HEIGHT % 2) == 0:
            maxPoints = int(BOARD_TILE_HEIGHT * BOARD_TILE_WIDTH / 2 + 1)
            print(maxPoints)
        else:
            maxPoints = int(BOARD_TILE_WIDTH * BOARD_TILE_HEIGHT // 2 + 1)
            print(maxPoints)
        return maxPoints

    #called every time an unmarked line is marked
    def handle_turn(self, line, ui, screen):
        if not line.isMarked:
            line.mark_line()
            self.check_point(ui, screen)
    
    #checks is any unclaimed square has been claimed after current turn
    #if claimed, score for current turn player, change square to match color.
    #if score, current player goes again. if no score, other player gets turn.
    def check_point(self, ui, screen):
        points = 0
        for square in self.dotBoard.squares:
            if square.check_square():
                if self.playerOneTurn:
                    square.color = square.p1Color
                    square.owner = 1
                else:
                    square.color = square.p2Color
                    square.owner = 2
                points += 1
        if points > 0:
            if self.playerOneTurn:
                self.playerOneScore += points
            else:
                self.playerTwoScore += points
        else:
            self.playerOneTurn = not self.playerOneTurn
            ui.changeTurn(screen, self.playerOneTurn)
        ui.updateScore(self, screen)


#main game logic
def main():
    #Pygame & windows setup
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill('white')
    pygame.display.set_caption('Dots and squares')
    #firstload used to skip winner display first time game loads
    firstLoad = True

    #shown when game loads and every time game is won
    def show_game_over(Screen, message = ""):
        font = pygame.font.Font(None, 50)
        #win message is generated on main game loop
        winMessage = font.render(message, True, "black", "white")
        winMessageRect = winMessage.get_rect()
        winMessageRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        #game over message, also displayed upon game launch
        goMessage = font.render("Press any key to start playing", True, "black", "white")
        goMessageRect = goMessage.get_rect()
        goMessageRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.fill(pygame.Color("white"))
        screen.blit(goMessage, goMessageRect)
        screen.blit(winMessage, winMessageRect)
        pygame.display.flip()

        #loop that runs while game over screen is active
        waiting = True
        while waiting:
            clock.tick(FPS)
            #handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    #MAIN GAME LOOP
    #game over starts as true to handle first game load
    game_over = True
    while True:
        
        if game_over:
            #if not first load, generate winner message and pass as optional parameter
            if not firstLoad:
                message = 'Player %s wins!' %("1" if game.playerOneScore > game.playerTwoScore else "2")
                show_game_over(screen, message)
            #if first load, display on 'start game' message
            else:
                show_game_over(screen)
                firstLoad = False
            game_over = False
            screen.fill(pygame.Color("white"))

            #CREATE GAME AND UI OBJECTS
            game = Game()
            ui = UI.UI(game)

        #handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #Handle mouse movement to provide feedback when player hovers overlines
            elif event.type == pygame.MOUSEMOTION:
                for line in game.dotBoard.lines:
                    if line.colideRect.collidepoint(pygame.mouse.get_pos()):
                        line.color = line.hoverColor
                    else:
                        line.color = line.defaultColor
            #Handle mouse clicks to see if player clicked on a line
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for line in game.dotBoard.lines:
                    if line.colideRect.collidepoint(pygame .mouse.get_pos()):
                        game.handle_turn(line, ui, screen)

        #check if player has gotten more than half of points,
        #if so declare winner and end game
        if game.playerOneScore >= game.scoreToWin or game.playerTwoScore >= game.scoreToWin:
            game_over = True

        #call dot board draw
        game.dotBoard.draw_board(screen)

        #call UI draw
        ui.drawUI(screen)

        pygame.display.update()
        clock.tick(FPS)


#call main function to start game
if __name__ == "__main__":
    main()