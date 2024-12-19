import random
RTCOLORS = ["Red", "Black"]

class RouletteLogics:
    """
    RouletteLogics class is used to define the logics can be used to place bets in roulette game.
    """
    def __init__(self, bpsarg, bet_history: list[dict]):
        """
        Initialize the RouletteLogics class with the given arguments.

        Args:
            bpsarg: The argument to be used in the logic.
            bet_history: The history of the bets placed.
        """
        self.bpsarg = bpsarg
        self.bet_history = bet_history
        self.last_bet = bet_history[-1] if bet_history else None
    
    def last_color_again(self):
        """
        Returns the color of the last turns winning number.
        """
        return self.last_bet["Bet Outcome"]["Color"]
    
    def reverse_last_color(self):
        """
        Returns the opposite color of the last turns winning number.
        """
        if self.last_bet["Bet Outcome"]["Color"] == "Red":
            return "Black"
        return "Red"

    def random_color(self):
        """
        Returns a random color from the RTCOLORS list.
        """
        return random.choice(RTCOLORS)

roulette_logic_dict = {
    "always_red": RouletteLogics("Red", []),
    "always_black": RouletteLogics("Black", []),
    "always_green": RouletteLogics("Green", []),
    "random_color": RouletteLogics(RTCOLORS, []),
}


         


