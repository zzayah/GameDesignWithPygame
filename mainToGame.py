from game import Game
from board import Board
board = Board((9, 9))
screenSize = (board.getSize()[0]*16, board.getSize()[1]*16)
game = Game(board, screenSize)
game.run()
