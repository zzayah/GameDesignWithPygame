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
            num = math.floor(random.random()*6 + 1)
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
found_match = True
start_turn_init = True

# game conditions
start = True

num_players = int(input("How many people are playing (1-4)?"))

for index in range(num_players):
    name = input(f"Enter a name for player {index + 1}:")
    add = Player(name)
    name_list.append(add)

print(name_list)

while start:
    for player_index in range(len(name_list)):
        current_player = name_list[player_index]
        current_player.roll_die()
        all_rolls = current_player.get_rolls()
        print(current_player)
        while start_turn_init:
            for i in range(6):
                if current_space == all_rolls[i]:
                    # remove, increment space, make player role a 0, reset loop to check
                    current_player.remove_chips(1)
                    current_space += 1
                    all_rolls[i] = 0
                    found_match = True
                    gameboardMod[i] = "X"
                    i = 0

                    if gameboardMod == ["X", "X", "X", "X", "X", "X"]:
                        print(f"Player {current_player} WON! Game finished.")
                        start = False

                    print(gameboard)
                    print(gameboardMod)
                    print(all_rolls)
                    print(current_space)
                    print(current_player)
                    print(i)

        if not found_match:
            current_player.remove_chips(7-current_space)


