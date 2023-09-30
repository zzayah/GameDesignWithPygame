from game import Game
from board import Board

size = (14, 9)
prob = 0.1
board = Board(size, prob)
screenSize = (board.getSize()[1]*16 + 100, board.getSize()[0]*16 + 100)
print(screenSize)
game = Game(board, screenSize)
game.run()


