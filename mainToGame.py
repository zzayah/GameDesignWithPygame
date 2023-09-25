from game import Game
from board import Board
size = (9, 9)
prob = 0.5
board = Board(size, prob)
screenSize = (board.getSize()[0]*16, board.getSize()[1]*16)
game = Game(board, screenSize)
game.run()
