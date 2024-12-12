import random
import Player
import utils
import betamountstrats

class Roulette:
    def __init__(self, wheel: tuple, players: list):
        self.data = {
            "Game Data": {
                "Rounds Played": 0,
                "Wagered": 0,
                "Hands Won by Players": 0,
                "Hands Lost by Players": 0,
                "Casino Profit": 0
            },
            "Player Data": {
                "Profited Players": 0,
                "Lost Players": 0,
                "Profited Player's Total Gain": 0
            },
        }
        
        self.overall_data = {
            "Overall Data": {
                "Overall Rounds Played": 0,
                "Overall Wagered": 0,
                "Overall Hands Won by Players": 0,
                "Overall Hands Lost by Players": 0,
                "Overall Casino Profit": 0
            },
        }

        self.wheel = wheel
        self.players = players
        self.active_players = players.copy()
        self.betted_players = []

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
        properties['Column'] = ['1st', '2nd', '3rd'][(spun_number - 1) % 3]

        if spun_number <= 12:
            properties['Dozen'] = '1st'
        elif spun_number <= 24:
            properties['Dozen'] = '2nd'
        else:
            properties['Dozen'] = '3rd'

        return properties

    def get_bets(self):
        self.betted_players = []
        for player in self.active_players[:]:
            if player.place_bet():
                self.betted_players.append(player)
                self.data["Game Data"]["Wagered"] += player.bet_history[-1]['Bet Amount']
            else:
                self.active_players.remove(player)

    def evaluate_bets(self, spun_number: int):
        results = self.num_properties(spun_number)
        for player in self.betted_players:
            if not player.bet_history:
                continue
            player_bet = player.bet_history[-1]
            bet_place = player_bet['Bet Place']
            if bet_place in results.values():
                winnings = player_bet['Bet Amount'] * 2
                player.current_bal += winnings
                self.data["Game Data"]["Hands Won by Players"] += 1
            else:
                self.data["Game Data"]["Hands Lost by Players"] += 1
        
    def calc_data(self):
        for player in self.players:
            self.data["Game Data"]["Casino Profit"] += player.starting_balance - player.current_bal
            if player.current_bal > player.starting_balance:
                self.data["Player Data"]["Profited Player's Total Gain"] += player.current_bal - player.starting_balance
    
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

    def print_results(self):
        for player in self.players:
            print(f"Player's Starting Balance: {player.starting_balance} - Player's Ending Balance: {player.current_bal}")
        for data in self.data:
            print(f"{data}:")
            for key, value in self.data[data].items():
                print(f"    {key}: {value}")

    def reset_data(self):
        self.data = {
            "Game Data": {
                "Rounds Played": 0,
                "Wagered": 0,
                "Hands Won by Players": 0,
                "Hands Lost by Players": 0,
                "Casino Profit": 0
            },
            "Player Data": {
                "Profited Players": 0,
                "Lost Players": 0,
                "Profited Player's Total Gain": 0
            },
        }

        for player in self.players:
            player.reset_player()
        
        self.active_players = self.players.copy()

    def roulette_sim_multiple(self, sim_times: int):
        for _ in range(sim_times):
            self.roulette_simulator()
            for key, value in self.data["Game Data"].items():
                self.overall_data["Overall Data"][f"Overall {key}"] += value
            self.reset_data()

def random_color():
    return random.choice(['Red', 'Black'])

# Example setup
ali = Player.Player(
    starting_bal=1000, 
    starting_bet=0, 
    stop_win=2000, 
    stop_loss=0, 
    bet_amount_strategy=betamountstrats.all_in, 
    bet_placement_strategy=random_color, 
    bps_argument=None
)

players = [ali]
rt = Roulette(utils.european_wheel, players)
rt.roulette_sim_multiple(200000)
print(rt.overall_data)