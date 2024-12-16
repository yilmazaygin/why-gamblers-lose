import random
roulette_utils = {
    "european_wheel": (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26),
    "american_wheel": (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 37, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2),
    "triplezero_wheel": (38, 0, 37, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26),
    "general_payrates": {"Straight":36, "Split":18, "Street":12, "Corner":9, "Five-Line":7, "Six-Line":6, "Column":3, "Dozen":3, "Red/Black":2, "Odd/Even":2, "Low/High":2, },
    "Color": ("Red", "Black"),
    "High/Low": ("High", "Low"),
    "Odd/Even": ("Odd", "Even"),
    "Dozen": ("1st Dozen", "2nd Dozen", "3rd Dozen"),
    "Column": ("1st Column", "2nd Column", "3rd Column")
    #May add streets or corners too?
}

class GeneralStrats:
    def __init__(self):
        pass
    
    @staticmethod
    def random_that(that: tuple):
        return random.choice(that)
    
    @staticmethod
    def always_that(that: str):
        return(that)
    
class BetAmountStrats:
    def __init__(self):
        pass

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
        "all_in": all_in,
        "flat_bet": flat_bet,
        "martingale": martingale,
        "reverse_martingale": reverse_martingale,
        "dalembert": dalembert,
        "reverse_dalembert": reverse_dalembert,
        "oscars_grind": oscars_grind,
        "fibonacci": fibonacci,
        "reverse_fibonacci": reverse_fibonacci,
        "one_three_two_six": one_three_two_six,
        "grand_martingale": grand_martingale,
        "reverse_grand_martingale": reverse_grand_martingale,
        "paroli": paroli,
        "reverse_paroli": reverse_paroli
    }
