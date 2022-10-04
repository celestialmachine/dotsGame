#Programmer: Victor Diaz
#I state the code submitted is my own

import re
from turtle import position
import pygame
import main
import copy
import random

#DotBoard class creates the board grid and draws dots
class DotBoard:
    #Constructor
    def __init__(self) -> None:
        self.board = []
        self.lines = []
        self.squares = []
        #popualte self.board with positions of all dots
        for y in range(main.BOARD_TILE_HEIGHT + 1):
            self.board.append([])
            for x in range(main.BOARD_TILE_WIDTH +1 ):
                self.board[y].append([self.starting_point()[0] + (x * main.TILE_SIZE),
                                    self.starting_point()[1] + (y * main.TILE_SIZE)])
        #Populate line and square collections
        self.create_lines()
        self.create_squares()
    
    #gets coordinates for dots
    def starting_point(self):
        return [(main.SCREEN_WIDTH / 2) - ((main.BOARD_TILE_WIDTH * main.TILE_SIZE) / 2),
                (main.SCREEN_HEIGHT / 2) - ((main.BOARD_TILE_HEIGHT * main.TILE_SIZE) / 2)]
    
    #function creates all lines
    def create_lines(self):
        #Create all vertical lines
        for i in range(main.BOARD_TILE_HEIGHT):
            for j in range(main.BOARD_TILE_WIDTH + 1):
                self.lines.append(Line(self.board[i][j], True))
        #Create all horizontal lines
        for i in range(main.BOARD_TILE_HEIGHT + 1):
            for j in range(main.BOARD_TILE_WIDTH):
                self.lines.append(Line(self.board[i][j], False))
    
    #function creates all squares
    def create_squares(self):
        for y in range(main.BOARD_TILE_HEIGHT):
            for x in range(main.BOARD_TILE_WIDTH):
                self.squares.append(Square(self.board[y][x], (x, y), self.lines))
    
    #Draws squares, lines, and dots on board
    def draw_board(self, screen):
        for square in self.squares:
            square.draw_square(screen)
        for line in self.lines:
            line.draw_tick(screen)
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                pygame.draw.circle(screen, (20, 20, 20),
                 (self.board[x][y][0], self.board[x][y][1]),
                 main.DOT_SIZE, 0)
        
    
#tick line class
class Line:
    def __init__(self, position, isVertical) -> None:
        self.startPosition = position
        self.isVertical = isVertical
        self.isMarked = False
        self.color = (240, 240, 240)
        self.defaultColor = (240, 240, 240)
        self.hoverColor = (120, 120, 120)
        self.markedColor = (0, 0, 0)
        self.colideBufferWidth = 10
        self.colideBufferLength = 20
        self.colideRect = self.make_colide_rectangle()
        self.drawRect = self.make_draw_rectangle()

    #Draw rectacngle is what is displayed on the screen
    def make_draw_rectangle(self):
        if self.isVertical:
            rect = pygame.Rect(self.startPosition[0] - (main.LINE_WIDTH / 2),
                                self.startPosition[1], main.LINE_WIDTH, main.TILE_SIZE)
            return rect
        else:
            rect = pygame.Rect(self.startPosition[0], self.startPosition[1]
                                - (main.LINE_WIDTH /2), main.TILE_SIZE, main.LINE_WIDTH)
            return rect
    
    #Collision rectangle is what is used to check for line selection
    #Collision rectangle is wider than draw rectangle so it is easier to select
    def make_colide_rectangle(self):
        if self.isVertical:
            rect = pygame.Rect(self.startPosition[0] - ((main.LINE_WIDTH + self.colideBufferWidth) / 2),
                                self.startPosition[1] + (self.colideBufferLength / 2),
                                main.LINE_WIDTH + (self.colideBufferWidth),
                                main.TILE_SIZE - (self.colideBufferLength))
            return rect
        else:
            rect = pygame.Rect(self.startPosition[0] + (self.colideBufferLength / 2),
                                self.startPosition[1] - ((main.LINE_WIDTH + self.colideBufferWidth) / 2),
                                main.TILE_SIZE - (self.colideBufferLength),
                                main.LINE_WIDTH + (self.colideBufferWidth))
            return rect

    #Draws line object on screen
    def draw_tick(self, screen):
        pygame.draw.rect(screen, self.color, self.drawRect)
    
    #called when line is selected by player
    def mark_line(self):
        self.defaultColor, self.hoverColor, self.color = self.markedColor
        self.isMarked = True

#class
class Square:
    def __init__(self, Position, BoardPosition, Lines) -> None:
        self.position = Position
        #owner is player: 0 = default/no owner, 1 = player one score, 2 = player two score
        self.owner = 0
        self.color = "grey"
        self.p1Color = "blue"
        self.p2Color = "red"
        self.drawRect = pygame.Rect(self.position[0], self.position[1], main.TILE_SIZE, main.TILE_SIZE)
        self.edgeLines = [None] * 4
        self.fill_edges(Lines, BoardPosition)

    #draws square on screen
    def draw_square(self, screen):
        pygame.draw.rect(screen, self.color, self.drawRect)

    #Get surrounding lines of the square and stores refrence of them for score checking
    def fill_edges(self, lines, boardPosition):
        #add top tick
        self.edgeLines[0] = lines[(((main.BOARD_TILE_WIDTH * main.BOARD_TILE_HEIGHT) + main.BOARD_TILE_HEIGHT)
                            + boardPosition[0] + (boardPosition[1] * main.BOARD_TILE_WIDTH))]
        #add right tick
        self.edgeLines[1] = lines[(boardPosition[0] + (boardPosition[1] * main.BOARD_TILE_WIDTH) + 1 + (1 * boardPosition[1]))]
        #add bottom tick
        self.edgeLines[2] = lines[(((main.BOARD_TILE_WIDTH * main.BOARD_TILE_HEIGHT) + main.BOARD_TILE_HEIGHT)
                            + boardPosition[0] + (boardPosition[1] * main.BOARD_TILE_WIDTH) + main.BOARD_TILE_WIDTH)]
        #add left tick
        self.edgeLines[3] = lines[(boardPosition[0] + (boardPosition[1] * main.BOARD_TILE_WIDTH) + (1 * boardPosition[1]))]

    #check square to see if enclosed
    def check_square(self):
        #only check if no owner, skip squares already claimed
        if self.owner < 1:
            pointCheck = []
            for edge in self.edgeLines:
                pointCheck.append(edge.isMarked)
            if all(pointCheck):
                return True
        else:
            return False