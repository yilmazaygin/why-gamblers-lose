import Player
import RouletteTable


class Game():
    def __init__(self):
        self.players = [] # player list
        self.roulette_table = RouletteTable.RouletteTable()

    # init players
    def init_players(self):
        pass

    def play_round(self):
        for player in self.players:
            player.place_bet(player.placed_number)

        number = self.roulette_table.spin_the_wheel()
        color = self.roulette_table.check_spun_number_properties(number)['Color']
        for player in self.players:
            if color == self.roulette_table.check_spun_number_properties(player.placed_number)['Color']:
                player.current_bal += self.roulette_table.payrates['Color'] * player.current_bet
                player.last_bet_condition = False
            else:
                player.last_bet_condition = True

        print(number, color)




g = Game()

g.players.append(Player.Player(500, 1, 100000, 0, 'martingale'))

for i in range(0,1000):
    g.play_round()
    for player in g.players:
        print("Balance: ", player.current_bal, "Bet: ", player.current_bet)


        