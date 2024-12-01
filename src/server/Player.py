import RouletteTable

class Player:
    def __init__(self, starting_bal, starting_bet, stop_win, stop_loss, strategy,):
        self.starting_bal = starting_bal
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.strategy = strategy

        self.bet_history = []
        self.current_bal = starting_bal
        self.current_bet = starting_bet

    def place_bet(self, number):
        pass