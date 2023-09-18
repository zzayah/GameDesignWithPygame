import random

class Player:
    name = None
    chips = None
    roll = None

    def __init__(self, name):
        self.name = name
        self.chips = 10
        self.roll = None

    def roll(self, num):
        self.roll = sorted([random.randint(1, 6) for _ in range(num)])



class Board:
    # Computational Comparison
    board = None
    # Tracks where in "open" the game is
    count = None
    # List of 6 boolean values to track weather a space is available or not
    open = None

    def __init__(self):
        self.board = [_ for _ in range(1, 7)]
        self.count = 0
        self.open = [True for _ in range(6)]

    def reset(self):
        self.board = [_ for _ in range(1, 7)]
        self.count = 0
        self.open = [True for _ in range(6)]

    def check(self, roll: list):
        score = 0
        flag = False
        for i in range(len(roll)):
            if roll[i] == self.board[0]:
                self.board.pop(0)
                self.open[self.count] = False
                self.count += 1
                flag = True
                if len(self.board) == 0:
                    self.reset()
                    return -1
            else:
                score += 1
        if flag:
            return 0
        return score

    def printboard(self):
        finish = ["F", "I", "N", "I", "S", "H"]
        finishstrike = ["F̶", "I̶", "N̶", "I̶", "S̶", "H̶"]
        for i in range(6):
            if self.open[i]:
                print(finish[i], end=" ")
            else:
                print(finishstrike[i], end=" ")
        print()
        