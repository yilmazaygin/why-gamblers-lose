import random # Importing the random module to generate random numbers

class RouletteTable: # The RouletteTable class
    european_wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
    payrates = {"Number":36, "Color":2, "Odd/Even":2, "Low/High":2, "Column":3, "Dozen":3} # The payrates for the different types of bets

    def __init__(self, payrates, wheel):
        self.payrates = self.payrates 
        self.wheel = self.european_wheel

    def spin_the_wheel(self): # The spin_the_wheel method
        return random.choice(self.wheel)
    
    def check_spun_number_properties(self, spun_number): # The check_spun_number_properties method
        properties = {'Number': None, 'Color': None, 'Odd/Even': None, 'Low/High': None, 'Column': None, 'Dozen': None}
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

        if spun_number is {0}:
            properties = {'Number': spun_number, 'Color': 'Green', 'Odd/Even': 'N/A', 'Low/High': 'N/A', 'Column': 'N/A', 'Dozen': 'N/A'}
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
