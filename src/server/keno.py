import random
import Player, betamountstrats

class Keno:
    basic_paytable = {0: 0, 1: 0, 2: 0, 3: 5, 4: 20, 5: 50, 6: 200, 7: 1000, 8: 5000, 9: 15000, 10: 50000}
    
    def __init__(self, rules=None):
        self.numbers = list(range(1, 81))

        default_rules = {
            "Numbers To Select": 10,
            "Numbers To Draw": 20,
            "Payout Table": self.basic_paytable
        }

        self.rules = {**default_rules, **(rules or {})}

    def draw_numbers(self):
        return random.sample(self.numbers, self.rules["Numbers To Draw"])

    def select_numbers(self, selected_numbers: list):
        if len(selected_numbers) != self.rules["Numbers To Select"]:
            raise ValueError("Invalid number of selected numbers")
        if any(number not in self.numbers for number in selected_numbers):
            raise ValueError("Invalid number selected")
        if len(set(selected_numbers)) != len(selected_numbers):
            raise ValueError("Duplicate numbers selected")
        return selected_numbers

    def check_winnings(self, selected_numbers: list, drawn_numbers: list):
        matching_numbers = set(selected_numbers).intersection(drawn_numbers)
        return len(matching_numbers), self.rules["Payout Table"].get(len(matching_numbers), 0)

    def keno_simulator(self, player: object):
        pass

