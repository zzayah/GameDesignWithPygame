import random

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 10

class FinishGame:
    def __init__(self, players):
        self.players = players
        self.num_players = len(players)
        self.gameboard = {i: None for i in range(1, 7)}
        self.current_player_index = 0

    def roll_dice(self, num_dice):
        return [random.randint(1, 6) for _ in range(num_dice)]

    def play_round(self):
        current_player = self.players[self.current_player_index]
        input(f"{current_player.name}, press Enter to roll your dice...")

        dice_rolls = self.roll_dice(6)
        print(f"{current_player.name} rolled: {dice_rolls}")

        added_numbers = []
        for roll in dice_rolls:
            if roll in self.gameboard and self.gameboard[roll] is None:
                self.gameboard[roll] = current_player.name
                added_numbers.append(roll)

        print("Gameboard:")
        for number, player in self.gameboard.items():
            print(f"{number}: {player or '-'}")

        if added_numbers == list(range(1, 7)):
            for player in self.players:
                if player != current_player:
                    player.chips -= 1
                    current_player.chips += 1
            print(f"{current_player.name} completed the row! {current_player.name} gets chips from other players.")

        elif len(added_numbers) != 0:
            chips_to_pay = 6 - len(added_numbers)
            current_player.chips -= chips_to_pay
            print(f"{current_player.name} must pay {chips_to_pay} chips to the pot.")

        self.current_player_index = (self.current_player_index + 1) % self.num_players

    def run_game(self):
        while len(self.players) > 1:
            self.play_round()
            if self.players[self.current_player_index].chips <= 0:
                print(f"{self.players[self.current_player_index].name} is out of chips and out of the game!")
                self.players.pop(self.current_player_index)
                if self.current_player_index == len(self.players):
                    self.current_player_index = 0

        winner = self.players[0]
        print(f"Congratulations, {winner.name}! You are the last player standing and win the pot!")

if __name__ == "__main__":
    num_players = int(input("Enter the number of players (3-5): "))
    if 3 <= num_players <= 5:
        players = [Player(f"Player {i+1}") for i in range(num_players)]
        game = FinishGame(players)
        game.run_game()
    else:
        print("Invalid number of players. The game supports 3 to 5 players.")
