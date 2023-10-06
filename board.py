from piece import Piece
from random import random


class Board:
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.lost = False
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.bombAry = []
        self.flagAry = []
        self.numFlags = 0
        self.setBoard()

    def setBoard(self):
        self.board = []
        _flagAryRow = []
        _bombAryRow = []

        for row in range(self.size[0]):
            row_list = []
            for col in range(self.size[1]):

                _flagAryRow.append(False)

                hasBomb = random() < self.prob
                if hasBomb:
                    _bombAryRow.append(True)  # Add True to boardAry to indicate a bomb
                else:
                    _bombAryRow.append(False)  # Add False to boardAry to indicate no bomb
                    self.numNonBombs += 1
                piece = Piece(hasBomb)
                row_list.append(piece)
            self.board.append(row_list)
            self.bombAry.append(_bombAryRow)
            self.flagAry.append(_flagAryRow)
        self.setNeighbors()

    def getTotalBombs(self):
        return self.numBombs

    def setNeighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListOfNeighbors((row, col))
                piece.setNeighbors(neighbors)

    def getListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or outOfBounds:
                    continue
                neighbors.append(self.getPiece((row, col)))
        return neighbors

    def getSize(self):
        return self.size

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, rightClick, index=None):
        flags_around = sum(1 for neighbor in piece.getNeighbors() if neighbor.getFlagged())

        if piece.getClicked():
            if flags_around == piece.getNumAround():
                for neighbor in piece.getNeighbors():
                    if not neighbor.getClicked() and not neighbor.getFlagged():
                        neighbor_index = self.getPieceIndex(neighbor)
                        self.handleClick(neighbor, False, neighbor_index)  # Pass the index parameter

        elif rightClick:
            piece.toggleFlag()
            self.flagAry[index[0]][index[1]] = True
            if piece.getFlagged():
                self.numFlags += 1
            elif not piece.getFlagged():
                self.numFlags -= 1
            return

        if piece.getFlagged():
            return

        piece.click()
        if piece.getHasBomb():
            self.lost = True
            return

        self.numClicked += 1
        if piece.getNumAround() != 0:
            return

        for neighbor in piece.getNeighbors():
            if not neighbor.getHasBomb() and not neighbor.getClicked():
                neighbor_index = self.getPieceIndex(neighbor)
                self.handleClick(neighbor, False, neighbor_index)  # Pass the index parameter

    def getPieceIndex(self, piece):
        for row_idx, row in enumerate(self.board):
            if piece in row:
                col_idx = row.index(piece)
                return (row_idx, col_idx)
        return None

    def handleClickGameDisabled(self):
        self.setBoard()
        self.lost = False
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0

    def getLost(self):
        return self.lost

    def getWon(self):
        return self.numNonBombs == self.numClicked

    def getNumFlags(self):
        return self.numFlags

    def getStatusRevert(self):
        self.lost = False
        self.won = False

    def resetBoard(self):
        self.lost = False
        self.won = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.bombAry = []
        self.flagAry = []
        self.setBoard()  # Reset the game board to its initial state