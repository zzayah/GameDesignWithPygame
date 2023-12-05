import csv
import pygame as pg
import tile

class Main:

    def __init__(self, filename):
        self.board_names = []
        self.board_tiles
        self.filename
        self.current_pos = []
        self.running = True
        self.first_turn = False
        self.screen = None

    def set_board(self):
        with open(f"{self.filename}.txt", "r") as ins:
            self.board_names = [[str(t) for t in line.split()] for line in ins]
        
        for row in range(9):
            for col in range(9):
                self.board_tiles[row][col] = tile(f"{self.board_names[row][col]}")

    def draw(self):
        if self.first_turn:
            # tiles are 64 x 64 (= 576) and y coordinate is gives 20 pixels of room
            screen = pg.display.set_mode((776, 616))
            screen.fill((255, 255, 255))
            # screen.blit()

        for row in range(9):
            for col in range(9):
                return
        
    
    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                else:
                    self.draw()
            
