import utils
import player
import random
import math

class PlayerCreators:
    def __init__(self):
        self.config = { # Configurations for player creation
            "Balance": { # Starting balance values
                "Low": (500, 1000), 
                "Low-Mid": (1001, 2000),
                "Mid": (2001, 5000),
                "Mid-High": (5001, 10000),
                "High": (10001, 20000),
                "Very High": (20001, 50000),
            },
            "Goal": { # Stop Win and Stop Loss values, percentage of balance
                "Low": {
                    "Stop Win": (1.3, 1.75), # %130 - %175
                    "Stop Loss": (0.3, 0.5), # 30% - 50%
                },
                "Low-Mid": {
                    "Stop Win": (1.75, 2.25), # 175% - 225%
                    "Stop Loss": (0.5, 0.75), # 50% - 75%
                },
                "Mid": {
                    "Stop Win": (2.25, 3.00), # 225% - 300%
                    "Stop Loss": (0.75, 1.00), # 75% - 100%
                },
                "Mid-High": {
                    "Stop Win": (3.00, 4.00), # 300% - 400%
                    "Stop Loss": (0.75, 1.00), # 75% - 100%
                },
                "High": {
                    "Stop Win": (4.00, 5.00), # 400% - 500%
                    "Stop Loss": (1.00, 1.00), # 100%
                },
                "Very High": {
                    "Stop Win": (5.00, 10.00), # 500% - 1000%
                    "Stop Loss": (1.00, 1.00), # 100%
                },
            },
            "Bet Amount": { # First bet amount, percentage of balance
                "Low": (0.005, 0.01), # 0.5% - 1%
                "Low-Mid": (0.01, 0.03), # 1% - 3%
                "Mid": (0.03, 0.5), # 3% - 5%
                "Mid-High": (0.05, 0.07), # 5% - 7%
                "High": (0.07, 0.10), # 7% - 10%
                "Very High": (0.10, 0.15), # 10% - 15%
            },
        }

    @staticmethod
    def all_bas(attrs: tuple): # All attiributes are same, except bet_amount_strategy
        all_bas_players = []
        for bet_strat_key, bet_strat_value in utils.betamountstrats_dict.items():
            player_instance = player.Player(
                attrs[0],  # starting_bal
                attrs[1],  # starting_bet
                attrs[2],  # stop_win
                attrs[3],  # stop_loss
                bet_strat_value,  # bet_amount_strategy
                attrs[4],  # bet_placement_strategy
                attrs[5]   # bps_argument
            )
            all_bas_players.append(player_instance)
        return all_bas_players
    
    @staticmethod
    def all_bps(attrs: tuple): # All attiributes are same, except bet_placement_strategy, NEEDS A BPS ARGUMENT!
        all_bps_players = []
        for logic_strat_key, logic_strat_value in utils.logicstrats_dict.items():
            player_instance = player.Player(
                attrs[0],  # starting_bal
                attrs[1],  # starting_bet
                attrs[2],  # stop_win
                attrs[3],  # stop_loss
                attrs[4],  # bet_amount_strategy
                logic_strat_value,  # bet_placement_strategy
                attrs[5]   # bps_argument
            )
            all_bps_players.append(player_instance)
        return all_bps_players
    
    def all_bas_all_bps(attrs: tuple): # All attiributes are same, except bet_amount_strategy and bet_placement_strategy, NEEDS A BPS ARGUMENT!
        all_bas_all_bps_players = []
        for bet_strat_key, bet_strat_value in utils.betamountstrats_dict.items():
            for logic_strat_key, logic_strat_value in utils.logicstrats_dict.items():
                player_instance = player.Player(
                    attrs[0],  # starting_bal
                    attrs[1],  # starting_bet
                    attrs[2],  # stop_win
                    attrs[3],  # stop_loss
                    bet_strat_value,  # bet_amount_strategy
                    logic_strat_value,  # bet_placement_strategy
                    attrs[4]   # bps_argument
                )
                all_bas_all_bps_players.append(player_instance)
        return all_bas_all_bps_players
    
    def bal_chooser(self, bal_range: tuple): # Returns a random balance value
        lower, upper = self.config["Balance"][bal_range]
        return random.randint(lower, upper-1)  # Tamsayı döndürür

    def goal_chooser(self, goal_range): # Returns a random stop win and stop loss values
        stop_win_range_lower, stop_win_range_upper = self.config["Goal"][goal_range]["Stop Win"]
        stop_loss_range_lower, stop_loss_range_upper = self.config["Goal"][goal_range]["Stop Loss"]
        
        stop_win = round(random.uniform(stop_win_range_lower, stop_win_range_upper), 2)
        stop_loss = round(random.uniform(stop_loss_range_lower, stop_loss_range_upper), 2)
        
        return (stop_win, stop_loss)

    def bet_amount_chooser(self, bal_range): # Returns a random bet amount
        bet_amount_range_lower, bet_amount_range_upper = self.config["Bet Amount"][bal_range]
        bet_amount = round(random.uniform(bet_amount_range_lower, bet_amount_range_upper), 3)
        print(bet_amount)
        return bet_amount

    def random_player_creator(self): # Creates a player with random attributes
        bal_range = random.choice(list(self.config["Balance"].keys()))
        starting_bal = self.bal_chooser(bal_range)
        starting_bet = int(starting_bal * self.bet_amount_chooser(bal_range))
        stop_win, stop_loss = self.goal_chooser(bal_range)
        stop_win = int(stop_win * starting_bal)
        stop_loss = int((starting_bal / stop_win) * 100)

        bet_amount_strategy = random.choice(list(utils.betamountstrats_dict.values()))
        bet_placement_strategy = random.choice(list(utils.logicstrats_dict.values()))
        bps_argument = "BPSARG"

        player_instance = player.Player(
            starting_bal,
            starting_bet,
            stop_win,
            stop_loss,
            bet_amount_strategy,
            bet_placement_strategy,
            bps_argument
        )
        return player_instance
