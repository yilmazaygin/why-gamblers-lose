class BetAmountStrats:
    """
    This class defines various betting strategies.
    Each method implements a specific betting strategy.
    """

    def __init__(self, current_balance: int, starting_bet: int, bet_history: list[dict]):
        """
        Initialize the class with the current balance, starting bet, and bet history.

        Args:
            current_balance (int): Current balance of the player.
            starting_bet (int): Initial bet amount.
            bet_history (list[dict]): List of dictionaries containing the bet history
        """
        self.current_balance = current_balance
        self.starting_bet = starting_bet
        self.bet_history = bet_history
    
        # Initialize the next bet amount, wich will be adjusted by the strategy
        self.next_bet = 0
        # Check the last bet condition, if any
        self.last_bets_condition = bet_history[-1]['Bet Condition'] if len(bet_history) > 0 else None
        # Check the last bet amount, if any
        self.last_bet_amount = bet_history[-1]['Bet Amount'] if len(bet_history) > 0 else None

    def check_bet_history(self) -> bool:
        """
        This method checks the bet history, if its empty, it sets the next bet to the starting bet.
        
        Returns:
            bool: True if the bet history is not empty, False otherwise.
        """
        if len(self.bet_history) == 0:
            self.next_bet = self.starting_bet
            return False
        return True

    def flat_bet(self) -> int:
        """
        This strategy bets the same amount every time.
        """
        return self.starting_bet
    
    def all_in(self) -> int:
        """
        This strategy bets the entire balance every time.
        """
        return self.current_balance
    
    def ten_percent(self) -> int:
        """
        This strategy bets 10% of the current balance every time.
        """
        self.next_bet = int(self.current_balance * 0.1)
        return self.next_bet
    
    def five_percent(self) -> int:
        """
        This strategy bets 5% of the current balance every time.
        """
        self.next_bet = int(self.current_balance * 0.05)
        return self.next_bet
    
    def martingale(self) -> int:
        """
        This strategy doubles the bet amount after every loss.
        """
        if self.check_bet_history():
            if self.last_bets_condition == True:
                self.next_bet = self.starting_bet
            else:
                self.next_bet = self.last_bet_amount * 2
        return self.next_bet
    
    def reverse_martingale(self) -> int:
        """
        This strategy doubles the bet amount after every win.
        """
        if self.check_bet_history():
            if self.last_bets_condition == False:
                self.next_bet = self.starting_bet
            else:
                self.next_bet = self.last_bet_amount * 2
        return self.next_bet
        
    def grand_martingale(self) -> int:
        """
        This strategy doubles the bet amount and adds the starting bet after every loss.
        """
        if self.check_bet_history():
            if self.last_bets_condition == True:
                self.next_bet = self.starting_bet
            else:
                self.next_bet = self.last_bet_amount * 2 + self.starting_bet
        return self.next_bet
    
    def reverse_grand_martingale(self) -> int:
        """
        This strategy doubles the bet amount and adds the starting bet after every win.
        """
        if self.check_bet_history():
            if self.last_bets_condition == False:
                self.next_bet = self.starting_bet
            else:
                self.next_bet = self.last_bet_amount * 2 + self.starting_bet
        return self.next_bet

    def dalembert(self) -> int:
        """
        This strategy increases the bet amount by 1 after every loss and decreases it by 1 after every win.
        """
        if self.check_bet_history():
            if self.last_bets_condition == True:
                self.next_bet = self.last_bet_amount - 1    
            else:
                self.next_bet = self.last_bet_amount + 1
        return self.next_bet
    
    def reverse_dalembert(self) -> int:
        """
        This strategy increases the bet amount by 1 after every win and decreases it by 1 after every loss.
        """
        if self.check_bet_history():
            if self.last_bets_condition == False:
                self.next_bet = self.last_bet_amount - 1
            else:
                self.next_bet = self.last_bet_amount + 1
        return self.next_bet
    
    def oscars_grind(self) -> int:
        """
        This strategy increases the bet amount by 1 after every win and keeps it the same after every loss.
        """
        if self.check_bet_history():
            if self.last_bets_condition == False:
                self.next_bet = self.last_bet_amount
            else:
                self.next_bet = self.last_bet_amount + 1
        return self.next_bet
    
    def one_three_two_six(self) -> int:
        """
        This strategy is a positive progression strategy that uses a sequence of numbers to determine the bet amount.
        """
        if self.check_bet_history():
            if not self.last_bets_condition: 
                self.next_bet = self.starting_bet
        
            if self.last_bet_amount == self.starting_bet:
                self.next_bet = self.starting_bet * 3
            elif self.last_bet_amount == self.starting_bet * 3:
                self.next_bet = self.starting_bet * 2
            elif self.last_bet_amount == self.starting_bet * 2:
                self.next_bet = self.starting_bet * 6
            else:
                self.next_bet = self.starting_bet
        return self.next_bet
    
    def fibonacci(self) -> int:
        """
        This strategy is a positive progression strategy that uses the Fibonacci sequence to determine the bet amount.
        """
        if self.check_bet_history():
            if not self.last_bets_condition:
                if self.last_bet_amount == self.starting_bet:
                    self.next_bet = self.starting_bet * 2
                else:
                    self.next_bet = self.last_bet_amount + self.bet_history[-2]["Bet Amount"]
            else:
                if self.last_bet_amount in [self.starting_bet, self.starting_bet * 2]:
                    self.next_bet = self.starting_bet
                else:
                    self.next_bet = self.bet_history[-3]["Bet Amount"]
        return self.next_bet
    
    def reverse_fibonacci(self) -> int:
        """
        This strategy is a negative progression strategy that uses the Fibonacci sequence to determine the bet amount.
        """
        if self.check_bet_history():
            if self.last_bets_condition:
                if self.last_bet_amount == self.starting_bet:
                    self.next_bet = self.starting_bet * 2
                else:
                    self.next_bet = self.last_bet_amount + self.bet_history[-2]["Bet Amount"]
            else:
                if self.last_bet_amount in [self.starting_bet, self.starting_bet * 2]:
                    self.next_bet = self.starting_bet
                else:
                    self.next_bet = self.bet_history[-3]["Bet Amount"]
        return self.next_bet
    
    def paroli(self) -> int:
        """
        This strategy is a similar to to reverse martingale, but it resets after 3 wins.
        """
        if self.check_bet_history():
            if not self.last_bets_condition:
                self.next_bet = self.starting_bet
            else:
                if self.last_bet_amount == self.starting_bet:
                    self.next_bet = self.starting_bet * 2
                elif self.last_bet_amount == self.starting_bet * 2:
                    self.next_bet = self.starting_bet * 4
                else:
                    self.next_bet = self.starting_bet
        return self.next_bet
    
    def reverse_paroli(self) -> int:
        """
        This strategy is a similar to to martingale, but it resets after 3 losses.
        """
        if self.check_bet_history():
            if self.last_bets_condition:
                self.next_bet = self.starting_bet
            else:
                if self.last_bet_amount == self.starting_bet:
                    self.next_bet = self.starting_bet * 2
                elif self.last_bet_amount == self.starting_bet * 2:
                    self.next_bet = self.starting_bet * 4
                else:
                    self.next_bet = self.starting_bet
        return self.next_bet
    
bas_dict = {
    "flat_bet": lambda instance: instance.flat_bet(),
    "all_in": lambda instance: instance.all_in(),
    "ten_percent": lambda instance: instance.ten_percent(),
    "five_percent": lambda instance: instance.five_percent(),
    "martingale": lambda instance: instance.martingale(),
    "reverse_martingale": lambda instance: instance.reverse_martingale(),
    "grand_martingale": lambda instance: instance.grand_martingale(),
    "reverse_grand_martingale": lambda instance: instance.reverse_grand_martingale(),
    "dalembert": lambda instance: instance.dalembert(),
    "reverse_dalembert": lambda instance: instance.reverse_dalembert(),
    "oscars_grind": lambda instance: instance.oscars_grind(),
    "one_three_two_six": lambda instance: instance.one_three_two_six(),
    "fibonacci": lambda instance: instance.fibonacci(),
    "reverse_fibonacci": lambda instance: instance.reverse_fibonacci(),
    "paroli": lambda instance: instance.paroli(),
    "reverse_paroli": lambda instance: instance.reverse_paroli()
}

def get_bet_amount_strat(strategy: str, instance: BetAmountStrats) -> int:
    """
    This function returns the bet amount based on the selected strategy.

    Args:
        strategy (str): The name of the betting strategy.
        instance (BetAmountStrats): An instance of the BetAmountStrats class.

    Returns:
        int: The bet amount based on the selected strategy.
    """
    return bas_dict[strategy](instance)
