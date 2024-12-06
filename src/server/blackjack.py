import random

class BlackJack:
    payrates = {}

    def __init__(self, deck_amount, other_player_amount): # Constructor
        self.deck_amount = deck_amount
        self.other_player_amount = other_player_amount 

        self.simulation_history = []
        self.game_history = []

    def deck_creator(self, deck_amount): # Deck Creator, returns the deck_amount times the deck
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        deck = [rank + " of " + suit for suit in suits for rank in ranks]
        deck = deck * deck_amount
        return deck

    def shuffle_deck(self, deck): # Shuffles the Deck, returns the shuffled deck
        random.shuffle(deck)
        return deck

    def value_of_hand(self, hand): # Ace can be 1 or 11
        pass
        
    def basic_strategy(self):
        pass

    def player_play(self):
        pass

    def dealer_play(self):
        pass

    def blackjack_simulator(self, player):
        deck = self.deck_creator(8)
        deck = self.shuffle_deck(deck)

        print("Player Start Balance:", player.current_bal)
        game_condition = True
        
        while game_condition:
            if len(deck) <= 52:
                game_condition = False
                break

            can_player_bet = player.place_bet()
            if not can_player_bet:
                game_condition = False
                break

            dealer_hand = []
            simulated_player_hand = []
            player1 =[]
            player2 = []
