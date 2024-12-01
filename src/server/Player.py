import RouletteTable

class Player:
    def __init__(self, starting_bal, starting_bet, stop_win, stop_loss, bet_amount_strategy, bet_placement_strategy):
        self.starting_bal = starting_bal
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.bet_amount_strategy = bet_amount_strategy()
        self.bet_placement_strategy = bet_placement_strategy()

        self.bet_history = []
        self.current_bal = starting_bal

    def place_bet(self, number):
        if self.current_bal <= self.stop_loss:
            return "You have reached your stop loss limit. You cannot place any more bets."
        if self.current_bal >= self.stop_win:
            return "You have reached your stop win limit. You cannot place any more bets."
        
        bet_amount = self.bet_amount_strategy()
        bet_placement = self.bet_placement_strategy()

        if bet_amount > self.current_bal:
            return "You do not have enough funds to place this bet."
        if bet_amount > RouletteTable.min_bet:
            return "The bet amount is below the minimum bet amount."
        if bet_amount > RouletteTable.max_bet:
            return "The bet amount is above the maximum bet amount."
        
        self.bet_history.append() # Add a new dictionary to the bet_history list
        self.bet_history[-1]["Bet Amount"] = bet_amount 
        self.bet_history[-1]["Bet Type"] = bet_placement
        self.bet_history[-1]["Bet Condition"] = bet_placement == number
        pass