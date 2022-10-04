#Programmer: Victor Diaz
#I state the code submitted is my own

import pygame
import main

class UI:
    #UI constructor
    def __init__(self, Game) -> None:
        self.font = pygame.font.Font(None, 60)
        self.caption = pygame.font.Font(None, 30)
        #Player X Turn display
        self.turn = self.font.render('Player 1 Turn', True, "grey", "white")
        self.turnRect = self.turn.get_rect()
        self.turnRect.center = (main.SCREEN_WIDTH //2, main.SCREEN_HEIGHT // 12)
        #Player 1 score display
        self.p1Score = self.font.render(f'P1 Score: {Game.playerOneScore}', True, "blue", "white")
        self.p1ScoreRect = self.p1Score.get_rect()
        self.p1ScoreRect.center = (main.SCREEN_WIDTH // 4, main.SCREEN_HEIGHT // 8 * 7)
        #Player 2 score display
        self.p2Score = self.font.render(f'P2 Score: {Game.playerOneScore}', True, "red", "white")
        self.p2ScoreRect = self.p1Score.get_rect()
        self.p2ScoreRect.center = (main.SCREEN_WIDTH // 4 * 3, main.SCREEN_HEIGHT // 8 * 7)
        #Score to win display
        self.scoreToWin = self.caption.render(f'Score to win: {Game.points_to_win()}', True, "grey", "white")
        self.scoreToWinRect = self.scoreToWin.get_rect()
        self.scoreToWinRect.center = (main.SCREEN_WIDTH // 2, main.SCREEN_HEIGHT // 20 * 19)

    def drawUI(self, screen):
        screen.blit(self.turn, self.turnRect)
        screen.blit(self.p1Score, self.p1ScoreRect)
        screen.blit(self.p2Score, self.p2ScoreRect)
        screen.blit(self.scoreToWin, self.scoreToWinRect)
    
    def updateScore(self, Game, Screen):
        Screen.fill(pygame.Color("white"))
        self.p1Score = self.font.render(f'P1 Score: {Game.playerOneScore}', True, "blue", "white")
        self.p2Score = self.font.render(f'P2 Score: {Game.playerTwoScore}', True, "red", "white")
        
    def changeTurn(self, screen, isP1Turn):
        screen.fill(pygame.Color("white"))
        self.turn = self.font.render('Player %s Turn' %("1" if isP1Turn else "2"), True, "grey", "white")