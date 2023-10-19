import pygame as pg
from board import Board

class Main:
    
    def __init__(self):
        self.board = Board()
        self.screen = pg.set_mode(316, 316) # each block 64 x 64 and spaces are 20 x 64 (width x height)