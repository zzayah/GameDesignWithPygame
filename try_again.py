import random

class Player:

    def __init__(self, name):
        self.chips = 10
        self.name = name

    def remove_chips(self, remove):
        self.chips -= remove
    
    def get_chips(self):
        return self.chips
    
    def add_chips(self, add):
        self.chips += add


# setup
player_list = []

num_players = int(input("How many people are playing (3-5)?"))

for index in range(num_players):
    name = input(f"Enter a name for player {index + 1}:")
    add = Player(name)
    player_list.append(add)

print(player_list)

# game environment
gameboard = ["O", "O", "O", "O", "O", "O"]
continue_game = True

# die
def roll_die():
    return [random.randint(1, 6) for _ in range(6)]

while continue_game:

    for cur_player in player_list:

        # player regulation
        match_found = False


        print(f"{cur_player.name}, press Enter to roll the die")
        roll = roll_die()
        print("{cur_player.name} rolled {roll}")

        # computational
        roll.sort()
        comp_roll = roll.copy()
        for i in range(1, 7):
            if comp_roll.count(i) > 1:
                for each in range(comp_roll.count(i)-1):
                    comp_roll.remove(i)
        print(f"Computational: {comp_roll}")

        # board interation for current player

        for num in comp_roll:

            if gameboard[0] == "O" and num == 1:
                gameboard[0] = "X"
                cur_player.remove_chips(1)
                match_found = True
                print("{current_player.name} matched 1")

                continue
            elif gameboard[1] == "O" and num == 2 and gameboard[0] == "X":
                gameboard[1] = "X"
                cur_player.remove_chips(1)
                match_found = True
                print("{current_player.name} matched 2")
                continue
            elif gameboard[2] == "O" and num == 3 and gameboard[1] == "X":
                gameboard[2] = "X"
                cur_player.remove_chips(1)
                match_found = True
                print("{current_player.name} matched 3")
                continue
            elif gameboard[3] == "O" and num == 4 and gameboard[2] == "X":
                gameboard[3] = "X"
                cur_player.remove_chips(1)
                match_found = True
                print("{current_player.name} matched 4")
                continue
            elif gameboard[4] == "O" and num == 5 and gameboard[3] == "X":
                gameboard[4] = "X"
                cur_player.remove_chips(1)
                match_found = True
                print("{current_player.name} matched 5")
                continue
            elif gameboard[5] == "O" and num == 6 and gameboard[4] == "X":
                gameboard[5] = "X"
                cur_player.remove_chips(1)
                match_found = True
                print("{current_player.name} matched 6")
                continue
            elif not match_found:
                print("No matches found")
                cur_player.remove_chips(gameboard.count("O"))
                print(f"{cur_player.name} owes {gameboard.count('O')} chips")
                continue

        # mid game
        if gameboard.count("O") == 0:
            print("Gameboard is full")
            for each in player_list:
                if each.name != cur_player.name:
                    each.remove_chips(1)

        # end game
        for player in player_list:
            if player.get_chips() == 0:
                player_list.remove(player)
                print(f"{player.name} has no more chips")

            if len(player_list) == 1:
                print(f"{player_list[0].name} wins!")
                continue_game = False
                break