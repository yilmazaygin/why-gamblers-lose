import random
import player
import utils
from game import Game

class Roulette(Game): # Inherit from Game class
    def __init__(self, wheel: tuple, players: list, sim_times: int): # All usable wheels are in utils.roulette_utils
        super().__init__(players, "Roulette", sim_times) 
        self.wheel = wheel

    def spin_wheel(self): # Spins the wheel and returns the spun number
        return random.choice(self.wheel)

    def num_properties(self, spun_number: int): # Returns the properties of the spun number
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


    def roulette_simulator(self): # Simulates the roulette game, can be run multiple times
        for _ in range(self.sim_times):
            while self.active_players:
                self.get_bets()
                if not self.active_players:
                    break
                self.data["Game Data"]["Rounds Played"] += 1
                spun_number = self.spin_wheel()
                self.evaluate_bets_list(self.num_properties(spun_number))
            self.calc_data()
            self.add_to_overall_data()
            self.reset_data()


# Example usage
ali = player.Player(
    starting_bal=1000, 
    starting_bet=50, 
    stop_win=2000, 
    stop_loss=0, 
    bet_amount_strategy=utils.BetAmountStrats.flat_bet, 
    bet_placement_strategy=utils.LogicStrats.always_that, 
    bps_argument="Red"
)

veli = player.Player(
    starting_bal=1000, 
    starting_bet=50, 
    stop_win=4000, 
    stop_loss=0, 
    bet_amount_strategy=utils.BetAmountStrats.martingale, 
    bet_placement_strategy=utils.LogicStrats.always_that, 
    bps_argument="Black"
)

players = [ali, veli]
rt = Roulette(utils.roulette_utils["european_wheel"], players, 5)
rt.roulette_simulator()
print(rt.overall_data)
print(rt.last_data())
