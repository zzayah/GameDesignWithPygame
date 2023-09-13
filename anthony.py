import random


class Player:
    # Name of player
    name = None
    # Number of chips player holds
    chips = None
    # List that is the same size as the board with random numbers from 1 to 6
    roll = None

    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.roll = None

    # Generates a list of [num] random numbers from 1 to 6
    def rolldice(self, num):
        self.roll = sorted([random.randint(1, 6) for _ in range(num)])


class Board:
    # List of numbers from 1 to 6, used for comparing dice roll too
    board = None
    # Keeps track of where in "open" the game is
    count = None
    # List of 6 boolean values, default to true and represents if the letter is open
    open = None

    def __init__(self):
        self.board = [i for i in range(1, 7)]
        self.count = 0
        self.open = [True for _ in range(6)]

    # Resets the board to its default values
    def reset(self):
        self.board = [i for i in range(1, 7)]
        self.count = 0
        self.open = [True for _ in range(6)]

    # Checks [roll] against the board, returns:
    #   Number of chips due if no matches were found
    #   0 if matches were found and pops them off the board
    #   -1 if the board is empty and resets the board
    def check(self, roll: list):
        score = 0
        flag = False
        for i in range(len(roll)):
            if roll[i] == self.board[0]:
                self.board.pop(0)
                self.open[self.count] = False
                self.count = self.count + 1
                flag = True
                if len(self.board) == 0:
                    self.reset()
                    return -1
            else:
                score = score + 1
        if flag:
            return 0
        return score

    # Prints out the board using normal strikethrough letters
    def printboard(self):
        finish = ["F", "I", "N", "I", "S", "H"]
        finishstrike = ["F̶", "I̶", "N̶", "I̶", "S̶", "H̶"]
        for i in range(6):
            if self.open[i]:
                print(finish[i], end=" ")
            else:
                print(finishstrike[i], end=" ")
        print()


class Game:
    # List of player objects representing all players in the game
    players = None
    # Instantiation of board object
    board = None

    # Creates a board object and a list of [num] players, instantiating each with user input
    def __init__(self, num):
        self.players = [Player(input("Player " + str(i) + ", what is your name?\n"), 10) for i in range(1, num + 1)]
        self.board = Board()

    # Core game loop; rolls dice, runs the check method, and logic depending on the return
    def turn(self):
        for player in self.players:
            input("\n" + player.name + ", ready to roll the dice?\n")
            player.rolldice(len(self.board.board))
            print(player.name + ", your roll is " + str(player.roll))
            score = self.board.check(player.roll)
            if score == -1:
                for _ in range(len(self.players)):
                    player.chips = player.chips + 1
                for pplayer in self.players:
                    pplayer.chips = pplayer.chips - 1
                print("Board reached H and was reset! All players gave 1 chip to " + player.name + ".")
            if score == 0:
                print("No chips lost!")
            if score > 0:
                player.chips = player.chips - score
                print(str(score) + " chips were lost!")
            if player.chips <= 0:
                print(player.name + " was eliminated!")
                self.players.remove(player)
            print(player.name + ", you have " + str(player.chips) + " chips.")
            print()
            self.board.printboard()
            print("Next number needed: " + str(self.board.board[0]))


# Main Method
def main():
    finish = Game(int(input("How many players?\n")))
    while len(finish.players) > 1:
        finish.turn()
    print("\nCongratulations! " + finish.players[0].name + ", you won the game!")


if __name__ == "__main__":
    main()