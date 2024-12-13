import random
import Player
import utils
import betamountstrats
from game import Game

class Roulette(Game):
    def __init__(self, wheel: tuple, players: list):
        super().__init__(players, "Roulette")
        self.wheel = wheel

    def spin_wheel(self):
        return random.choice(self.wheel)

    def num_properties(self, spun_number: int):
        properties = {
            'Number': None,
            'Color': None,
            'Odd/Even': None,
            'Low/High': None,
            'Column': None,
            'Dozen': None
        }
        red_numbers = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)

        if spun_number in (0, 37, 38):
            properties = {
                'Number': "0" if spun_number == 0 else "00" if spun_number == 37 else "000",
                'Color': 'Green',
                'Odd/Even': 'N/A',
                'Low/High': 'N/A',
                'Column': 'N/A',
                'Dozen': 'N/A'
            }
            return properties

        properties['Number'] = spun_number
        properties['Color'] = 'Red' if spun_number in red_numbers else 'Black'
        properties['Odd/Even'] = 'Even' if spun_number % 2 == 0 else 'Odd'
        properties['Low/High'] = 'Low' if spun_number <= 18 else 'High'
        properties['Column'] = ['1st Column', '2nd Column', '3rd Column'][(spun_number - 1) % 3]

        if spun_number <= 12:
            properties['Dozen'] = '1st Dozen'
        elif spun_number <= 24:
            properties['Dozen'] = '2nd Dozen'
        else:
            properties['Dozen'] = '3rd Dozen'

        return properties

    def roulette_simulator(self):
        while self.active_players:
            self.get_bets()
            if not self.active_players:
                break

            self.data["Game Data"]["Rounds Played"] += 1
            spun_number = self.spin_wheel()
            self.evaluate_bets(spun_number)
        
        for player in self.players:
            if player.current_bal > player.starting_balance:
                self.data["Player Data"]["Profited Players"] += 1
            else:
                self.data["Player Data"]["Lost Players"] += 1
        self.calc_data()

    def roulette_sim_multiple(self, sim_times: int):
        for _ in range(sim_times):
            self.roulette_simulator()
            for key, value in self.data["Game Data"].items():
                self.overall_data["Overall Data"][f"Overall {key}"] += value
            self.reset_data()

# Example setup
ali = Player.Player(
    starting_bal=1000, 
    starting_bet=50, 
    stop_win=2000, 
    stop_loss=0, 
    bet_amount_strategy=betamountstrats.all_in, 
    bet_placement_strategy=utils.GeneralStrats.random_that, 
    bps_argument=utils.roulette_utils["Color"]
)

players = [ali]
rt = Roulette(utils.roulette_utils["european_wheel"], players)
rt.roulette_sim_multiple(100)
print(rt.overall_data)