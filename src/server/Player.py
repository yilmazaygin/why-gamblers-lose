import random
import utils

class Player:
    def __init__(self, starting_bal, starting_bet, stop_win, stop_loss, bet_amount_strategy, bet_placement_strategy, bps_argument: str):
        self.starting_balance = starting_bal
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.bet_amount_strategy = bet_amount_strategy
        self.bet_placement_strategy = bet_placement_strategy
        self.bps_argument = bps_argument

        self.player_overall_history =[]

        self.current_bal = starting_bal
        self.bet_history = []
        self.player_game_data = {
            "ID": f"{self.starting_balance}-{self.starting_bet}-X // {self.stop_win}-{self.stop_loss}-X",
            "ID2": f"{self.bet_amount_strategy.__name__}-{self.bet_placement_strategy.__name__}-{self.bps_argument}-X",
            "Ending Balance": 0,
            "Profit": 0,
            "Rounds Played": 0,
            "Bet History": self.bet_history
        }

    def place_bet(self): # Returns True if bet is placed, False if not
        if self.current_bal <= self.stop_loss: return False
        if self.current_bal >= self.stop_win: return False

        next_bet_amount = self.bet_amount_strategy(self)
        if next_bet_amount > self.current_bal: return False
        if self.bet_placement_strategy == None: return True # If no bet placement strategy is defined, return True. EDIT THIS LATER!
        if self.bps_argument == None:
            next_bet_placement = self.bet_placement_strategy()
        else:
            next_bet_placement = self.bet_placement_strategy(self.bps_argument)

        turns_bet = {"Bet Amount": next_bet_amount, "Bet Place": next_bet_placement, "Bet Condition": None, "Balance Before Bet": self.current_bal, "Balance After Bet": self.current_bal - next_bet_amount}
        self.bet_history.append(turns_bet)
        self.current_bal -=  next_bet_amount
        return True
    
    def reset_player(self): # Resets player's balance, bet history and game data
        self.bet_history = []
        self.current_bal = self.starting_balance
        self.player_overall_history.append(self.player_game_data)
        self.player_game_data = {
            "ID": f"{self.starting_balance}-{self.starting_bet}-X // {self.stop_win}-{self.stop_loss}-X",
            "ID2": f"{self.bet_amount_strategy.__name__}-{self.bet_placement_strategy.__name__}-{self.bps_argument}-X",
            "Ending Balance": 0,
            "Profit": 0,
            "Rounds Played": 0,
            "Bet History": self.bet_history
        }