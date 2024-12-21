import random
RTCOLORS = ["Red", "Black"]
BC_PLACES = ["Player", "Banker", "Tie"]

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
    
    def last_color_again(self) -> str:
        """
        Returns the color of the last turns winning number.
        """
        return self.last_bet["Bet Outcome"]["Color"]
    
    def reverse_last_color(self) -> str:
        """
        Returns the opposite color of the last turns winning number.
        """
        if self.last_bet["Bet Outcome"]["Color"] == "Red":
            return "Black"
        return "Red"

    def random_color(self) -> str:
        """
        Returns a random color from the RTCOLORS list.
        """
        return random.choice(RTCOLORS)

    def always_that(self):
        return self.bpsarg
    
roulette_logic_dict = {
    "last_winner": RouletteLogics(None, []),
    "reverse_last_color": RouletteLogics(None, []),
    "last_color_again": RouletteLogics(None, []),
    "random_color": RouletteLogics(RTCOLORS, []),
}

class BaccaratLogics:
    """
    BaccaratLogics class is used to define the logics can be used to place bets in baccarat game.
    """
    def __init__(self, bpsarg, bet_history: list[dict]):
        """
        Initialize the BaccaratLogics class with the given arguments.

        Args:
            bpsarg: The argument to be used in the logic.
            bet_history: The history of the bets placed.
        """
        self.bpsarg = bpsarg
        self.bet_history = bet_history
        self.last_bet = bet_history[-1] if bet_history else None

    def random_place(self) -> str:
        """
        Returns a random winner from the BACCARAT_PAYRATES keys.
        """
        return random.choice(BC_PLACES)

    def always_that(self) -> str:
        return self.bpsarg
         


