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