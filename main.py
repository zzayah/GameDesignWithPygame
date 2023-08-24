import random
import math


class Player:

    def __init__(self, name):
        self.name = name
        self.chips = 10
        self.rolls = [1, 1, 1, 1, 1, 1]

    def remove_chips(self, remove):
        self.chips -= remove

    def roll_die(self):
        # list of die rolls
        die_rolls = []
        for p in range(6):
            num = math.floor(random.random() * 6 + 1)
            die_rolls.append(num)
        self.rolls = die_rolls

    def get_rolls(self):
        return self.rolls


# setup
name_list = []

# game environment
gameboard = [1, 2, 3, 4, 5, 6]
gameboardMod = ["O", "O", "O", "O", "O", "O"]
current_space = 1
found_match = False
start_turn_init = True

# game conditions
start = True


# die
def roll_die(self):
    return [random.randomint(1, 6) for _ in range(6)]


num_players = int(input("How many people are playing (1-4)?"))

for index in range(num_players):
    name = input(f"Enter a name for player {index + 1}:")
    add = Player(name)
    name_list.append(add)

print(name_list)

while start:
    for player_index in range(len(name_list)):
        current_player = name_list[player_index]
        input(f"{current_player.name}, press Enter to roll the die")
        dice = roll_die().sort()

        print(f"{current_player.name} rolled {dice}")

        placed_die = []

        for board_index in gameboard:
            for roll_index in dice:
                if dice[roll_index] == 1 and gameboardMod[0] == "O":
                    found_match = True
                    gameboardMod[board_index] = "X"
                elif dice[roll_index] == gameboard[board_index] and board_index > 0 and gameboardMod[board_index-1] == "X":
                    found_match = True
                    gameboardMod[board_index] = "X"
                else:
                    break

