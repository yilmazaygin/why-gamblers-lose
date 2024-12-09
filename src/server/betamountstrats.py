
def all_in(self): # Goes all in every time
    return self.current_bal

def flat_bet(self): # Always bets the same amount
    return self.starting_bet

def martingale(self): # Doubles the bet every time it loses
    if not self.bet_history:
        return self.starting_bet
    
    return self.bet_history[-1]["Bet Amount"] * 2 if self.bet_history[-1]["Bet Condition"] == False else self.starting_bet

def reverse_martingale(self): # Doubles the bet every time it wins
    if self.bet_history == []:
        return self.starting_bet
    
    return self.bet_history[-1]["Bet Amount"] * 2 if self.bet_history[-1]["Bet Condition"] == True else self.starting_bet

def dalembert(self): # Increases the bet by 1 every time it loses, decreases it by 1 every time it wins
    if self.bet_history == []:
        return self.starting_bet
    
    return self.bet_history[-1]["Bet Amount"] + 1 if self.bet_history[-1]["Bet Condition"] == False else self.bet_history[-1]["Bet Amount"] - 1

def reverse_dalembert(self): # Increases the bet by 1 every time it wins, decreases it by 1 every time it loses
    if self.bet_history == []:
        return self.starting_bet
    
    return self.bet_history[-1]["Bet Amount"] + 1 if self.bet_history[-1]["Bet Condition"] == True else self.bet_history[-1]["Bet Amount"] - 1 

def oscars_grind(self): # Increases the bet by 1 every time it wins, keeps it the same every time it loses
    if self.bet_history == []:
        return self.starting_bet
    
    return self.bet_history[-1]["Bet Amount"] if self.bet_history[-1]["Bet Condition"] == False else self.bet_history[-1]["Bet Amount"] + 1

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
        
def grand_martingale(self): # Doubles the bet every time it loses, adds the starting bet to the bet after a loss, resets after a win
    if self.bet_history == []:
        return self.starting_bet
    
    return self.starting_bet if self.bet_history[-1]["Bet Condition"] == True else (self.bet_history[-1]["Bet Amount"] * 2) + self.starting_bet

def reverse_grand_martingale(self): # Doubles the bet every time it wins, adds the starting bet to the bet after a win, resets after a loss
    if self.bet_history == []:
        return self.starting_bet
    
    return self.starting_bet if self.bet_history[-1]["Bet Condition"] == False else (self.bet_history[-1]["Bet Amount"] * 2) + self.starting_bet

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
