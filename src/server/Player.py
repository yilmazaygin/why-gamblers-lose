import RouletteTable
import stratsfile
class Player:
    def __init__(self, starting_bal, starting_bet, stop_win, stop_loss, bet_amount_strategy, bet_color):
        self.starting_bal = starting_bal
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.bet_amount_strategy = stratsfile.bet_amount_strategies[bet_amount_strategy]
        self.bet_color = bet_color
        self.bet_history = []
        self.current_bal = starting_bal

    def place_bet(self, color):
        if self.current_bal <= 0:
            return False
        if self.stop_win <= self.current_bal:
            return False
        if self.stop_loss >= self.current_bal:
            return False
    
        bet_amount = self.bet_amount_strategy(self)
        if self.current_bal < bet_amount:
            return False

        bet_history_dict = dict()
        bet_history_dict["Bet Amount"] = bet_amount 
        bet_history_dict["Bet Type"] = color
        bet_history_dict["Bet Condition"] = None
        self.bet_history.append(bet_history_dict)
        return True
        

    def martingale(self): # Doubles the bet every time it loses
        if not self.bet_history:
            return self.starting_bet
    
        return self.bet_history[-1]["Bet Amount"] * 2 if self.bet_history[-1]["Bet Condition"] == False else self.starting_bet