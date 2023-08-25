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
gameboardMod = ["O", "O", "O", "O", "O", "O"]
start = True

# game conditions
start = True


# die
def roll_die():
    return [random.randint(1, 6) for _ in range(6)]


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
        dice = sorted(roll_die())

        print(f"{current_player.name} rolled {dice}")

        found_match = False

        for board_XO in gameboardMod:
            space_one_passed = False
            for dice_value in dice:
                if dice_value == 1 and gameboardMod[0] == "O" and board_XO == "O" and not space_one_passed:
                    found_match = True
                    gameboardMod[0] = "X"

                    current_player.remove_chips(1)
                    space_one_passed = True

                    print(f"{current_player.name} placed a 1 on the board.")
                elif dice_value == gameboardMod.index(board_XO) and gameboardMod[gameboardMod.index(board_XO) - 1] == "X":
                    found_match = True
                    current_player.remove_chips(1)
                    gameboardMod[gameboardMod.index(board_XO)] = "X"
                    print(f"{current_player.name} placed a {dice_value} on the board.")
                else:
                    break

        if all(status == "X" for status in gameboardMod):
            print(f"{current_player.name} won the ROUND! All other players owe them 1 chip!")

            for player in name_list:
                if player.chips == 1:
                    print(f"{player.name} ran out of chips! They are out!")
                    name_list.remove(player)
                    if len(name_list) == 1:
                        print(f"{name_list[0].name} won the whole GAME!")
                        start = False

        print(f"Gameboard: {gameboardMod}")
        print(f"Player chips:")
        for player in name_list:
            print(f"{player.name}: {player.chips} chips")
        input("Press Enter to continue to the next player...")
