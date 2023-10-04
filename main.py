from game import Game
from board import Board

size = (25, 25)
prob = .5
board = Board(size, prob)
screenSize = (board.getSize()[1]*16 + 100, board.getSize()[0]*16 + 100)
print(screenSize)
game = Game(board, screenSize)
game.run()


