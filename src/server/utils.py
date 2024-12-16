import random

payrates = { 
    # Payrates for each game
    "Roulette": {
        "Straigt": 36,
        "Split": 18,
        "Street": 12,
        "Corner": 9,
        "Five-Line": 7,
        "Six-Line": 6,
        "1st Column": 3, "2nd Column": 3, "3rd Column": 3,
        "1st Dozen": 3, "2nd Dozen": 3, "3rd Dozen": 3,
        "Odd": 2, "Even": 2,
        "High": 2, "Low": 2,
        "Black": 2, "Red": 2,

    },
    "Baccarat": {"Player": 2, 
                 "Tie": 9, 
                 "Banker": 1.95}
}

roulette_utils = {
    # Roulette utils
    "european_wheel": (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26),
    "american_wheel": (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 37, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2),
    "triplezero_wheel": (38, 0, 37, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26),
    "Column": ("1st Column", "2nd Column", "3rd Column"),
    "Dozen": ("1st Dozen", "2nd Dozen", "3rd Dozen"),
    "Odd/Even": ("Odd", "Even"),
    "High/Low": ("High", "Low"),
    "Color": ("Red", "Black"),
    #May add streets or corners too?
}

baccarat_utils = {
    # Baccarat utils
    "Player or Banker" : ("Player", "Banker"),
    "All Places": ("Player", "Tie", "Banker"),
}


class LogicStrats: # General strategies that can be used in any game
    
    @staticmethod
    def random_that(that: tuple): # Randomly chooses a value from a tuple
        return random.choice(that)
    
    @staticmethod
    def always_that(that: str): # Always chooses a specific value, must be string
        return(that)
    
class BetAmountStrats: # Strategies for determining the bet amount

    @staticmethod
    def all_in(self): # Goes all in every time
        return self.current_bal

    @staticmethod
    def flat_bet(self): # Always bets the same amount
        return self.starting_bet

    @staticmethod
    def martingale(self): # Doubles the bet every time it loses
        if not self.bet_history:
            return self.starting_bet
        
        return self.bet_history[-1]["Bet Amount"] * 2 if self.bet_history[-1]["Bet Condition"] == False else self.starting_bet

    @staticmethod
    def reverse_martingale(self): # Doubles the bet every time it wins
        if self.bet_history == []:
            return self.starting_bet
        
        return self.bet_history[-1]["Bet Amount"] * 2 if self.bet_history[-1]["Bet Condition"] == True else self.starting_bet

    @staticmethod
    def dalembert(self): # Increases the bet by 1 every time it loses, decreases it by 1 every time it wins
        if self.bet_history == []:
            return self.starting_bet
        
        return self.bet_history[-1]["Bet Amount"] + 1 if self.bet_history[-1]["Bet Condition"] == False else self.bet_history[-1]["Bet Amount"] - 1

    @staticmethod
    def reverse_dalembert(self): # Increases the bet by 1 every time it wins, decreases it by 1 every time it loses
        if self.bet_history == []:
            return self.starting_bet
        
        return self.bet_history[-1]["Bet Amount"] + 1 if self.bet_history[-1]["Bet Condition"] == True else self.bet_history[-1]["Bet Amount"] - 1 

    @staticmethod
    def oscars_grind(self): # Increases the bet by 1 every time it wins, keeps it the same every time it loses
        if self.bet_history == []:
            return self.starting_bet
        
        return self.bet_history[-1]["Bet Amount"] if self.bet_history[-1]["Bet Condition"] == False else self.bet_history[-1]["Bet Amount"] + 1

    @staticmethod
    def fibonacci(self): # Adds the last two bets to get the next one, resets to the starting bet after a win
        if self.bet_history == []:
            return self.starting_bet
        
        if not self.bet_history[-1]["Bet Condition"]:
            if self.bet_history[-1]["Bet Amount"] == self.starting_bet:
                return self.starting_bet * 2
            else:
                return self.bet_history[-1]["Bet Amount"] + self.bet_history[-2]["Bet Amount"]
            
        else:
            if self.bet_history[-1]["Bet Amount"] in [self.starting_bet, self.starting_bet * 2]:
                return self.starting_bet
            else:
                return self.bet_history[-3]["Bet Amount"]
        
    @staticmethod
    def reverse_fibonacci(self): # Adds the last two bets to get the next one, resets to the starting bet after a loss
        if self.bet_history == []:
            return self.starting_bet
        
        if self.bet_history[-1]["Bet Condition"]:
            if self.bet_history[-1]["Bet Amount"] == self.starting_bet:
                return self.starting_bet * 2
            else:
                return self.bet_history[-1]["Bet Amount"] + self.bet_history[-2]["Bet Amount"]
            
        else:
            if self.bet_history[-1]["Bet Amount"] in [self.starting_bet, self.starting_bet * 2]:
                return self.starting_bet
            else:
                return self.bet_history[-3]["Bet Amount"]

    @staticmethod
    def one_three_two_six(self): # Bets 1, 3, 2, 6 times the starting bet, resets after a win, goes back to the start after a loss
        if self.bet_history == []:
            return self.starting_bet
        
        if not self.bet_history[-1]["Bet Condition"]:
            return self.starting_bet
        
        else:
            if self.bet_history[-1]["Bet Amount"] == self.starting_bet:
                return self.starting_bet * 3
            elif self.bet_history[-1]["Bet Amount"] == self.starting_bet * 3:
                return self.starting_bet * 2
            elif self.bet_history[-1]["Bet Amount"] == self.starting_bet * 2:
                return self.starting_bet * 6
            else:
                return self.starting_bet
            
    @staticmethod
    def grand_martingale(self): # Doubles the bet every time it loses, adds the starting bet to the bet after a loss, resets after a win
        if self.bet_history == []:
            return self.starting_bet
        
        return self.starting_bet if self.bet_history[-1]["Bet Condition"] == True else (self.bet_history[-1]["Bet Amount"] * 2) + self.starting_bet

    @staticmethod
    def reverse_grand_martingale(self): # Doubles the bet every time it wins, adds the starting bet to the bet after a win, resets after a loss
        if self.bet_history == []:
            return self.starting_bet
        
        return self.starting_bet if self.bet_history[-1]["Bet Condition"] == False else (self.bet_history[-1]["Bet Amount"] * 2) + self.starting_bet
    
    @staticmethod
    def paroli(self): # Basically martingale but goes back to the start after winning 3 times
        if self.bet_history == []:
            return self.starting_bet
        
        if not self.bet_history[-1]["Bet Condition"]:
            return self.starting_bet
        
        else:
            if self.bet_history[-1]["Bet Amount"] == self.starting_bet:
                return self.starting_bet * 2
            elif self.bet_history[-1]["Bet Amount"] == self.starting_bet * 2:
                return self.starting_bet * 4
            else:
                return self.starting_bet

    @staticmethod    
    def reverse_paroli(self): # Basically reverse martingale but goes back to the start after losing 3 times
        if self.bet_history == []:
            return self.starting_bet
        
        if self.bet_history[-1]["Bet Condition"]:
            return self.starting_bet
        
        else:
            if self.bet_history[-1]["Bet Amount"] == self.starting_bet:
                return self.starting_bet * 2
            elif self.bet_history[-1]["Bet Amount"] == self.starting_bet * 2:
                return self.starting_bet * 4
            else:
                return self.starting_bet

betamountstrats_dict = {
    # Bet amount strategies
    "all_in": BetAmountStrats.all_in,
    "flat_bet": BetAmountStrats.flat_bet,
    "martingale": BetAmountStrats.martingale,
    "reverse_martingale": BetAmountStrats.reverse_martingale,
    "dalembert": BetAmountStrats.dalembert,
    "reverse_dalembert": BetAmountStrats.reverse_dalembert,
    "oscars_grind": BetAmountStrats.oscars_grind,
    "fibonacci": BetAmountStrats.fibonacci,
    "reverse_fibonacci": BetAmountStrats.reverse_fibonacci,
    "one_three_two_six": BetAmountStrats.one_three_two_six,
    "grand_martingale": BetAmountStrats.grand_martingale,
    "reverse_grand_martingale": BetAmountStrats.reverse_grand_martingale,
    "paroli": BetAmountStrats.paroli,
    "reverse_paroli": BetAmountStrats.reverse_paroli
}

logicstrats_dict = {
    # Logic strategies
    "random_that": LogicStrats.random_that,
    "always_that": LogicStrats.always_that
}