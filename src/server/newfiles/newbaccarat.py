from newgame import Game
import random
import newutils

BACCARAT_PAYRATES = {
    "Player": 2, 
    "Banker": 1.95, 
    "Tie": 9
}

class Baccarat(Game):
    def __init__(self, players, sim_times, rules, deck_amount):
        """
        Initializes the Baccarat class with the players, simulation times, rules, and deck amount.

        Args:
            players (list): List of player objects.
            sim_times (int): Number of times the game will be simulated.
            rules (dict): Dictionary of the rules of the game, such as min or max bet amount.
            deck_amount (int): Number of decks in the shoe, default is 1.
        """
        super().__init__(players, sim_times, rules) # Inherit from Game class
        self.deck_amount = deck_amount

        # Initialize the hands and values of the player and the banker
        self.player_hand = []
        self.banker_hand = []
        self.player_value = 0
        self.banker_value = 0
        self.hands = [self.player_hand, self.banker_hand]
        self.shoe = []

    def check_deck_amount(self) -> None:
        """
        Checks if the deck amount is valid, raises an error if not.
        """
        if not isinstance(self.deck_amount, int) or self.deck_amount < 1 or self.deck_amount > 10:
            raise ValueError("Deck amount must be an integer between 1 and 10.")

    def bac_hand_value(self, hand: list) -> int:
        """
        Calculates the value of the hand for baccarat.
        Baccarat hand is the sum of the values of the cards modulo 10.

        Args:
            hand (list): The hand of cards to evaluate.

        Returns:
            int: The calculated hand value.
        """
        values = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 0, "Jack": 0, "Queen": 0, "King": 0}
        try:
            return sum(values[card.split(" ")[0]] for card in hand) % 10
        except KeyError as e:
            raise ValueError(f"Invalid card in hand: {e}")

    def should_player_draw(self) -> bool:
        """
        Determines if the player should draw a third card.

        Returns:
            bool: True if the player draws a third card, False otherwise.
        """
        return self.player_value <= 5

    def should_banker_draw(self, player_third_card=None) -> bool:
        """
        Determines if the banker should draw a third card according to baccarat rules.

        Args:
            player_third_card (int, optional): Value of the player's third card.

        Returns:
            bool: True if the banker draws a third card, False otherwise.
        """
        if self.banker_value <= 2:
            return True
        elif self.banker_value == 3:
            return player_third_card != 8
        elif self.banker_value == 4:
            return player_third_card in [2, 3, 4, 5, 6, 7]
        elif self.banker_value == 5:
            return player_third_card in [4, 5, 6, 7]
        elif self.banker_value == 6:
            return player_third_card in [6, 7]
        return False

    def determine_result(self) -> str:
        """
        Determines the result of the game according to the values of the player and the banker.

        Returns:
            str: Result of the game, "Player", "Banker", or "Tie".
        """
        if self.player_value > self.banker_value:
            return "Player"
        elif self.banker_value > self.player_value:
            return "Banker"
        return "Tie"

    def calculate_hand_values(self) -> None:
        """
        Calculates the values of the hands of the player and the banker.
        """
        self.player_value = self.bac_hand_value(self.player_hand)
        self.banker_value = self.bac_hand_value(self.banker_hand)

    def draw_cards(self) -> None:
        """
        Determines if the player and banker should draw third cards according to baccarat rules.
        """
        # Player draws first
        if self.should_player_draw():
            self.player_hand.append(self.shoe.pop())
            self.player_value = self.bac_hand_value(self.player_hand)

        # Banker's turn, based on player's third card if applicable
        player_third_card = self.player_hand[2] if len(self.player_hand) == 3 else None
        if self.should_banker_draw(player_third_card):
            self.banker_hand.append(self.shoe.pop())
            self.banker_value = self.bac_hand_value(self.banker_hand)

    def baccarat_simulator(self) -> None:
        """
        Simulates the game of Baccarat.
        Each player will reset themselves after each simulation.
        The game will reset itself after each simulation.
        """
        self.check_deck_amount()
        self.check_sim_times()

        for _ in range(self.sim_times):
            self.shoe = newutils.create_shoe(self.deck_amount)
            self.shoe = newutils.shuffle_shoe(self.shoe)

            while self.active_players:
                if len(self.shoe) <= 6: # EDIT THIS LATER ACCORDING TO BACCARAT RULES
                    self.shoe = newutils.create_shoe(self.deck_amount)
                    self.shoe = newutils.shuffle_shoe(self.shoe)

                self.get_bets()
                if not self.active_players:
                    break

                newutils.deal(self.shoe, self.hands, 2)
                self.calculate_hand_values()
                self.draw_cards()

                result = {"Result": self.determine_result()}
                self.evaluate_bets(result, BACCARAT_PAYRATES)
                newutils.reset_hands(self.hands, [0, 0])

            self.reset_game()
        self.calc_data()
