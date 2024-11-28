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
        self.last_bet_condition = None
        self.last_bet_amount = None

    def place_bet(self):
        if self.current_bal >= self.stop_win or self.current_bal <= self.stop_loss:
            return "Player Achieved Stop Conditions"
        else:
            current_bet = self.strategy()
            self.bet_history.append(current_bet)
            self.current_bal -= current_bet

    def martingale(self):
        return self.starting_bet if self.last_bet_condition == 1 else self.last_bet_amount * 2

    def play():
        pass