import csv
import pygame as pg
import tile
import copy

class Main:

    def __init__(self):
        self.board_names = []
        self.board_tiles
        self.filename
        self.current_pos = []
        self.running = True
        self.first_turn = False
        
        self.alteration_right = 0
        self.alteration_down = 0

    def set_board(self):
        with open(f"{self.filename}.txt", "r") as ins:
            self.board_names = [[str(t) for t in line.split()] for line in ins]
        
        height = len(self.board_names)
        width = len(self.baord_names[0])
        new_board = [[]]
        for row in range(height+5):
            for col in range(width+5):
                new_board[row][col] = "floor"
        
        for row in range(height):
            for col in range(width):
                new_board[row+5][col+5] = self.board_names[row][col]
        
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
                image_path = f"{self.board_tiles[row + (self.alteration_right)][col + (self.alteration_down)].get_type()}"
                tile_surf = pg.image.load(image_path)
                screen.blit(tile_surf, (64 * row + 100, 64 * col + 20))
                
    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.UP:
                    if self.alteration_down == 0:
                        return
                    elif self.alteration_down > 0:
                        self.alteration_down += 1
                    else:
                        print("self.alteration_down error")
                elif event.type == pg.DOWN:
                    self.alteration_down += 1
                elif event.type == pg.LEFT:
                    if self.alteration_right == 0:
                        return
                    elif self.alteration_right > 0:
                        self.alteration_right += 1
                    else:
                        print("self.alteration_right error")
                elif event.type == pg.RIGHT:
                    self.alteration_right += 1

            self.draw()
            pg.display.flip()
            
