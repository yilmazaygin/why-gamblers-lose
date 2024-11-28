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
        self.placed_number = 9
        self.last_bet_condition = False
        self.last_bet_amount = None

    def place_bet(self, number):
        self.placed_number = number
        if self.current_bal >= self.stop_win or self.current_bal <= self.stop_loss:
            self.current_bet = 0
        else:
            if self.strategy == 'martingale':
                self.current_bet = self.martingale()
            elif self.strategy == 'reverse_martingale':
                self.current_bet = self.reverse_martingale()
            elif self.strategy == 'fibonicci':
                self.current_bet = self.fibonacci()
            elif self.strategy == 'parlay':
                self.current_bet = self.parlay()
            
            self.bet_history.append(self.current_bet)
            self.current_bal -= self.current_bet

    def martingale(self):
        print(self.last_bet_condition)
        return self.starting_bet if self.last_bet_condition == False else self.bet_history[len(self.bet_history) - 1] * 2

    def reverse_martingale(self):
        pass
    def fibonacci(self):
        pass
    def parlay(self):
        pass

        

p1 = Player(500, 1, 550, 350, 'martingale')
