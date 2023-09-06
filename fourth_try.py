import random
import math

class Player:

    def __init__(self, name):
        self.name = name
        self.chips = 10
        self.rolls = [1, 1, 1, 1, 1, 1]

    def remove_chips(self, remove):
        self.chips -= remove

    def add_chips(self, add):
        self.chips += add
    
    def roll_die(self):
        # List of die rolls
        die_rolls = []
        for _ in range(6):
            num = math.floor(random.random() * 6 + 1)
            die_rolls.append(num)
        self.rolls = die_rolls
    
    def return_comp_rolls(self):
        # Return self.rolls with duplicates removed
        return list(set(self.rolls))
    
    def to_string(self):
        return f"{self.name}: {self.chips} chips"

# Setup
player_list = []

print("Welcome to Finish! How many people are playing (3-5)?")
num_players = int(input())

for index in range(num_players):
    name = input(f"Enter a name for player {index + 1}: ")
    add = Player(name)
    player_list.append(add)

print(player_list)

gameboard_XO = ["O", "O", "O", "O", "O", "O"]
gameboard_num = [1, 2, 3, 4, 5, 6]
found_match = False

continue_game = True
while continue_game:

    cur_index = 0
    for cur_player in player_list:
        cur_player.roll_die()
        comp_rolls = cur_player.return_comp_rolls()

        print(f"{cur_player.name} rolled {cur_player.rolls}")

        # Check for matches
        
        for roll in comp_rolls:
            if roll == gameboard_num[cur_index] and gameboard_XO[cur_index] == "O" and cur_index < 5:
                print(f"{cur_player.name} matched {roll}! {cur_player.name} gives a chip to the pot.")

                cur_player.remove_chips(1)

                gameboard_XO[cur_index] = "X"
                cur_index += 1
                found_match = True
            elif roll == gameboard_num[cur_index] and gameboard_XO[cur_index] == "O" and cur_index == 5:
                print(f"{cur_player.name} matched 6! {cur_player.name} gives a chip to the pot, and all the other players put a chip into the pot.")

                
        if not found_match:
                cur_player.remove_chips()

        for each in player_list:
                each.remove_chips(1)
                    
                if each.chips <= 0:
                    player_list.remove(each)
                    print(f"{each.name} has been eliminated!")
                    if len(player_list) == 1:
                        continue_game = False
                        print(f"{player_list[0].name} wins!")
                        break

                print(f"Current standings: {[player.to_string() for player in player_list]}")
                print(gameboard_XO)

                gameboard_XO[cur_index] = "X"
                cur_index += 1
                found_match = True
