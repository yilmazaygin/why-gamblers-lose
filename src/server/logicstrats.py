import random

class BaccaratLogics:
    def __init__(self, game_history):
        self.game_history = game_history

    def random_player_or_banker(self):
        return random.choice(["Player", "Banker"])
    
    #Try using them, probably cant. So edit
    def always_that(self, that:str):
        valid_choices = ["Player", "Tie", "Banker"]
        if that not in valid_choices:
            raise ValueError(f"Invalid input: {that}. Expected one of {valid_choices}.")
        else:
            return that
    
    def last_again(self):
        if self.game_history[-1]: return self.game_history[-1]
        else: return BaccaratLogics.random_player_or_banker
    
    def reverse_last(self):
        return "Banker" if self.game_history[-1]["Bet Type"] == "Player" else "Player"

class RouletteLogics:
    def __init__(self, wheel_history):
        self.wheel_history = wheel_history
    
    def random_color(self):
        return random.choice(["Red", "Black"])

    def random_that(self, that: list):
        if that not in [["Red", "Black"], ["High", "Low"], ["Odd", "Even"]]:
            raise ValueError(f"Invalid input: {that}. Expected one of [['Red', 'Black'], ['High', 'Low'], ['Odd', 'Even']].")
        return random.choice(that)

    def always_that(self, that: str):
        valid_choices = ["Red", "Black", "High", "Low", "Odd", "Even"]
        if that not in valid_choices:
            raise ValueError(f"Invalid input: {that}. Expected one of {valid_choices}.")
        return that
        
    def last_again(self, that: str):
        if that in ["Red", "Black"]:
            return self.wheel_history[-1]["Color"]
        elif that in ["High", "Low"]:
            return self.wheel_history[-1]["Low/High"]
        elif that in ["Odd", "Even"]:
            return self.wheel_history[-1]["Odd/Even"]
        else:
            raise ValueError(f"Invalid input: {that}. Expected 'Red', 'Black', 'High', 'Low', 'Odd', or 'Even'.")
    
    def reverse_last(self, that: str):
        if that == "Red":
            return "Black" if self.wheel_history[-1]["Color"] == "Red" else "Red"
        elif that == "High":
            return "Low" if self.wheel_history[-1]["Low/High"] == "High" else "High"
        elif that == "Odd":
            return "Even" if self.wheel_history[-1]["Odd/Even"] == "Odd" else "Odd"
        else:
            raise ValueError(f"Invalid input: {that}. Expected 'Red', 'Black', 'High', 'Low', 'Odd', or 'Even'.")

    def min_amount(self, that: list):
        if that in ["Red", "Black"]:
            return "Red" if sum(1 for entry in self.wheel_history if entry['Color'] == 'Red') < sum(1 for entry in self.wheel_history if entry['Color'] == 'Black') else "Black"
        elif that in ["High", "Low"]:
            return "High" if sum(1 for entry in self.wheel_history if entry['Low/High'] == 'Low') < sum(1 for entry in self.wheel_history if entry['Low/High'] == 'High') else "Low"
        elif that in ["Odd", "Even"]:
            return "Odd" if sum(1 for entry in self.wheel_history if entry['Odd/Even'] == 'Even') < sum(1 for entry in self.wheel_history if entry['Odd/Even'] == 'Odd') else "Even"
        else:
            raise ValueError(f"Invalid input: {that}. Expected 'Red', 'Black', 'High', 'Low', 'Odd', or 'Even'.")

