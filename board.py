import pygame as pg

class Board:

    def __init__(self):
        self.screen = pg.display.set_mode(316, 316)
        self.matrix = [[0 for _ in range(3)] for _ in range(3)]

    def draw(self):
        for row in range(3):
            for col in range(3):
                pass
