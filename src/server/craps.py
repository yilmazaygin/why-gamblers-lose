import random

class Craps:
    def __init__(self) -> None:
        pass

    def dice(self):
        dice_one = [0, 1, 2, 3, 4, 5, 6]
        dice_two = [0, 1, 2, 3, 4, 5, 6]
        random.choice(dice_one)
        random.choice(dice_two)
        return random.choice(dice_one) , random.choice(dice_two)
    
    