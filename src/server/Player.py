import random
import betamountstrats

class Player:
    def __init__(self, starting_bal, starting_bet, stop_win, stop_loss, bet_amount_strategy, bet_placement_strategy):
        self.starting_balance = starting_bal
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.bet_amount_strategy = bet_amount_strategy
        self.bet_placement_strategy = bet_placement_strategy

        self.current_bal = starting_bal
        self.bet_history = []

    def place_bet(self):
        if self.current_bal <= self.stop_loss: return False
        if self.current_bal >= self.stop_win: return False

        next_bet_amount = self.bet_amount_strategy(self)
        if next_bet_amount > self.current_bal: return False

        next_bet_placement = self.bet_placement_strategy(self)

        turns_bet = {"Bet Amount": next_bet_amount, "Bet Place": next_bet_placement, "Bet Condition": None}
        self.bet_history.append(turns_bet)
        self.current_bal -=  next_bet_amount
        return True
    
    def reset_player(self):
        self.bet_history = []
        self.current_bal = self.starting_balance

