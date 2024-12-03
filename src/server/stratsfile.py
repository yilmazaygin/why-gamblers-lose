bet = {"Round Number": 0, 
       "Bet Amount": 50, 
       "Bet Type": 0,
       "Balance Before Bet": 0,
       "Bet Condition": 0,
       "Balance After Bet": 0,
       }


bet_amount_strategies = dict()


def all_in(self): # Goes all in every time
    return self.balance

def flat_bet(self): # Always bets the same amount
    return self.starting_bet

# Needs a proportion to work
def constant_proportion(self): # Bets the same proportion of the balance every time
    return self.balance * self.proportion

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
        
def labouchere(self): # Adds the first and last numbers of a sequence to get the next bet, removes the numbers after a win, adds the last bet to the sequence after a loss
    if len(self.sequence) == 0:
        return "Empty Sequence"

    if not self.bet_history[-1]["Bet Condition"]:
        self.sequence.append(self.bet_history[-1]["Bet Amount"])
        return self.sequence[0] + self.sequence[-1]

    else:  
        if len(self.sequence) == 1:
            bet_amount = self.sequence.pop(0)
            return bet_amount
        self.sequence.pop(0)
        self.sequence.pop(-1)
        if len(self.sequence) == 0:
            return "Empty Sequence"
        
        return self.sequence[0] + self.sequence[-1]

###############################
    
def james_bond(self): # Bets 20 on 0, 14 on 19-36, 5 on 13-18
    pass

def andrucci(self): # Bets on a random number that has come up more often than others
    pass

def twenty_four_numbers(self): # Bets on 24 numbers
    pass
    

bet_amount_strategies['martingale'] = martingale
bet_amount_strategies['flat_bet'] = flat_bet