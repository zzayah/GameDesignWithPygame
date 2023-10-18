import pygame as pg

class Board:

    def __init__(self):
        self.matrix = [[0 for _ in range(3)] for _ in range(3)]

    def draw(self):
        return 0