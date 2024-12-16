import random
import utils

class Player:
    def __init__(self, starting_bal, starting_bet, stop_win, stop_loss, bet_amount_strategy, bet_placement_strategy, bps_argument):
        self.starting_balance = starting_bal
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.bet_amount_strategy = bet_amount_strategy
        self.bet_placement_strategy = bet_placement_strategy
        self.bps_argument = bps_argument

        self.current_bal = starting_bal
        self.bet_history = []
        self.player_game_data = {
            "ID": f"{self.bet_placement_strategy}.{self.starting_balance}.{self.starting_bet}",
            "Starting Balance": self.starting_balance,
            "Bet Amount Strategy": self.bet_amount_strategy,
            "Bet Placement Strategy": self.bet_placement_strategy,
            "Ending Balance": 0,
            "Profit": 0,
            "Rounds Played": 0
        }

    def place_bet(self):
        if self.current_bal <= self.stop_loss: return False
        if self.current_bal >= self.stop_win: return False

        next_bet_amount = self.bet_amount_strategy(self)
        if next_bet_amount > self.current_bal: return False
        if self.bet_placement_strategy == None: return True # !!!!
        if self.bps_argument == None:
            next_bet_placement = self.bet_placement_strategy()
        else:
            next_bet_placement = self.bet_placement_strategy(self.bps_argument)

        turns_bet = {"Bet Amount": next_bet_amount, "Bet Place": next_bet_placement, "Bet Condition": None, "Balance Before Bet": self.current_bal, "Balance After Bet": self.current_bal - next_bet_amount}
        self.bet_history.append(turns_bet)
        self.current_bal -=  next_bet_amount
        return True
    
    def reset_player(self):
        self.bet_history = []
        self.current_bal = self.starting_balance
        self.player_game_data = {
            "ID": f"{self.bet_placement_strategy}.{self.starting_balance}.{self.starting_bet}",
            "Starting Balance": self.starting_balance,
            "Bet Amount Strategy": self.bet_amount_strategy,
            "Bet Placement Strategy": self.bet_placement_strategy,
            "Ending Balance": 0,
            "Profit": 0,
            "Rounds Played": 0
        }

