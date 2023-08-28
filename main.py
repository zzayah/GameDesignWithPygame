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

        # for computational purposes
        # Create a list to store duplicate values for comparison
        duplicate_values = []
        comp_dice = dice.copy()
            
        for value_to_check in range(1, 7):
            count_of_value = comp_dice.count(value_to_check)
                
            if count_of_value > 1:
                duplicate_values.extend([value_to_check] * count_of_value)
                    
                times_to_remove = count_of_value - 1
                for _ in range(times_to_remove):
                    comp_dice.remove(value_to_check)

        print(f"{current_player.name} rolled {dice}")
        print(comp_dice)

        found_match = False
        space_one_passed = False
        chips_to_remove = 0

        iterations = 0

        for current_XO_val in gameboardMod:
            for current_dice_val in comp_dice:

                # Case 1
                if not space_one_passed and current_dice_val == 1:
                    space_one_passed = True
                    found_match = True
                    gameboardMod[0] = "X"
                    chips_to_remove += 1
                    print("Removed 1 chip (Case 1))")
                    break
                # Case 2
                elif space_one_passed and current_XO_val == "O" and gameboardMod[iterations - 1] == "X" and gameboardMod.index("O") == current_dice_val - 1:
                    found_match = True
                    gameboardMod[0] = "O"
                    chips_to_remove += 1
                    print("Removed 1 chip (Case 2)")
                    break
                elif not found_match:
                    chips_owed = gameboardMod.count("O")
                    print("No matches found")
                    print("{current_player.name} owes {chips_owed} chips")
                    break

                iterations += 1


                # reset
        space_one_passed = False

        if all(status == "X" for status in gameboardMod):
            print(f"{current_player.name} won the ROUND! All other players owe them 1 chip!")

            for player in name_list:
                if player.chips == 0:
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
