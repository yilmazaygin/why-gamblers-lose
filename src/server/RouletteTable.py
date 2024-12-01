import random

european_wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
american_wheel = (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 37, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2)
triplezero_wheel= (38, 0, 37, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)
payrates = {"Straight":36, "Split":18, "Street":12, "Corner":9, "Five-Line":7, "Six-Line":6, "Column":3, "Dozen":3, "Red/Black":2, "Odd/Even":2, "Low/High":2, }

class RouletteTable:
    def __init__(self,  wheel_type, max_bet, min_bet):
        self.wheel_type = wheel_type
        self.max_bet = max_bet
        self.min_bet = min_bet

    def spin_the_wheel(self):
        return random.choice(self.wheel_type)
    
    def check_spun_number_properties(self, spun_number):
        properties = {'Number': None, 'Color': None, 'Odd/Even': None, 'Low/High': None, 'Column': None, 'Dozen': None}
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

        if spun_number in  [0, 37, 38]:
            properties = {'Number': 0, 'Color': 'Green', 'Odd/Even': 'N/A', 'Low/High': 'N/A', 'Column': 'N/A', 'Dozen': 'N/A'}
            properties['Number'] = "00" if spun_number == 37 else properties['Number']
            properties['Number'] = "000" if spun_number == 38 else properties['Number']
            return properties

        properties['Number'] = spun_number
        properties['Color'] = 'Red' if spun_number in red_numbers else 'Black'
        properties['Odd/Even'] = 'Even' if spun_number % 2 == 0 else 'Odd'
        properties['Low/High'] = 'Low' if spun_number <= 18 else 'High'
        properties['Column'] = ['1st', '2nd', '3rd'][(spun_number - 1) % 3]

        if spun_number <= 12:
            properties['Dozen'] = '1st'
        elif spun_number <= 24:
            properties['Dozen'] = '2nd'
        else:
            properties['Dozen'] = '3rd'

        return properties
