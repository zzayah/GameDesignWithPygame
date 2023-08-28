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
        # list of die rolls
        die_rolls = []
        for p in range(6):
            num = math.floor(random.random() * 6 + 1)
            die_rolls.append(num)
        self.rolls = die_rolls
    
    def return_comp_rolls(self):
        #return self.rolls with duplicates removed
        to_return = list(set(self.rolls))
        return to_return


# setup
player_list = []

print("Welcome to Finish! How many people are playing (3-5)?")
num_players = int(input())

for index in range(num_players):
    name = input(f"Enter a name for player {index + 1}:")
    add = Player(name)
    player_list.append(add)

print(player_list)

# game environment
gameboardFINISH = ["F", "I", "N", "I", "S", "H"]
gameboardXO = ["O", "O", "O", "O", "O", "O"]
gameboard_one_to_six = [1, 2, 3, 4, 5, 6]

# game conditions
continue_game = True

while continue_game:

    current_index = 0
    found_match = False

    for cur_player in player_list:

        cur_player.roll_die()
        print(f"{cur_player.name} rolled {cur_player.rolls}")

        rolls_for_computation = cur_player.return_comp_rolls()
        print(rolls_for_computation)

        
        for roll in rolls_for_computation:
            
            if current_index == 0 and roll == gameboard_one_to_six[current_index] and gameboardXO[current_index] == "O":
                gameboardXO[0] = "X"
                cur_player.remove_chips(1)
                print(f"GameboardXO = {gameboardXO}")
                print(f"{cur_player.name} rolled a 1! An X has been placed on the board!")
                print(f"{cur_player.name} has {cur_player.chips} chips left")


                current_index += 1
                found_match = True
            elif current_index > 0 and roll == gameboard_one_to_six[current_index] and gameboardXO[current_index - 1] == "O":
                gameboardXO[current_index] = "X"
                cur_player.remove_chips(1)
                print(f"GameboardXO = {gameboardXO}")
                print(f"{cur_player.name} rolled a {roll}! An X has been placed on the board!")
                print(f"{cur_player.name} has {cur_player.chips} chips left")

                current_index += 1
                found_match = True
            
        
        if all(x == "X" for x in gameboardXO):
            print(f"{cur_player.name} wins the round! All other players owe 1 to the pot!")
            for player in player_list:
                if player != cur_player:
                    player.remove_chips(1)

        if cur_player.chips == 0 and player in player_list > 1:
            print(f"{cur_player.name} is out of chips and out of the game!")
            player_list.remove(cur_player)
        elif player_list == 0:
            print(f"{cur_player} is the winner!")
            continue_game = False

        

        # add 1 to current_index per each value of X present in the gameboardXO
        current_index = 0
        for XO in gameboardXO:
            if XO == "X":
                current_index += 1
        found_match = False
        continue_game = False
