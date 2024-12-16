import random
import player
import utils
from game import Game

class Baccarat(Game): # Baccarat Class
    def __init__(self, deck_amount: int, players: list): # Constructor
        super().__init__(players, "Baccarat") # Calls the constructor of the parent class
        self.deck_amount = deck_amount

        self.player_hand = []
        self.banker_hand = []
        self.player_value = 0
        self.banker_value = 0

    def value_of_hand(self, hand: list): # Calculates the value of the hand, returns the value
        value = 0
        values = {"Ace":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":0, "Jack":0, "Queen":0, "King":0}
        for card in hand:
            card_value = card.split(" ")[0]
            value += values[card_value]
        return value % 10

    def player_play(self, hand_value: int): # Player Play Logic, returns True or False for hitting
        if hand_value in [0, 1, 2, 3, 4, 5]:
            return True
        elif hand_value in [6, 7, 8, 9]:
            return False

    def banker_play(self, hand_value: int, player_third_card=None): # Banker Play Logic, returns True or False for hitting
        if hand_value in [0, 1, 2]:
            return True
        elif hand_value == 3:
            return player_third_card != 8 
        elif hand_value == 4:
            return player_third_card in [2, 3, 4, 5, 6, 7]
        elif hand_value == 5:
            return player_third_card in [4, 5, 6, 7]
        elif hand_value == 6:
            return player_third_card in [6, 7]
        elif hand_value == 7:
            return False
        else:
            return False
        
    def calc_result(self, player_value: int, banker_value: int): # Calculates the result of the game
        if player_value > banker_value:
            return "Player"
        elif banker_value > player_value:
            return "Banker"
        else:
            return "Tie"

    def reset_hands(self): # Resets the hands
        self.player_hand = []
        self.banker_hand = []

    def calc_values(self): # Calculates the values of the hands
        self.player_value = self.value_of_hand(self.player_hand)
        self.banker_value = self.value_of_hand(self.banker_hand)
        return self.player_value, self.banker_value

    def baccarat_deal(self, deck :list): # Deals the cards to the player and the banker
        self.deal(deck, [self.player_hand, self.banker_hand], 2)
    
    def if_play(self, deck: list): # If the player or the banker should play
        if self.player_play(self.player_value):
            self.player_hand.append(deck.pop())
            self.player_value = self.value_of_hand(self.player_hand)

        if self.banker_play(self.banker_value, self.player_hand[-1] if len(self.player_hand) > 2 else None):
            self.banker_hand.append(deck.pop())
            self.banker_value = self.value_of_hand(self.banker_hand)

    def baccarat_simulator(self, sim_times: int): # Baccarat Simulator
        for _ in range(sim_times):
            deck = self.deck_creator(8)
            deck = self.shuffle_deck(deck)

            while self.active_players:
                if len (deck) <= 52:
                    break

                self.get_bets()
                if not self.active_players:
                    break
                self.data["Game Data"]["Rounds Played"] += 1

                self.baccarat_deal(deck)
                self.if_play(deck)
                self.evaluate_bets_str(self.calc_result(self.player_value, self.banker_value))
                self.reset_hands()

            self.calc_data()
            for key, value in self.data["Game Data"].items():
                self.overall_data["Overall Data"][f"Overall {key}"] += value
            self.reset_data()

'''
# Example Usage
ali = player.Player(500, 10, 1000, 0, utils.BetAmountStrats.all_in, utils.LogicStrats.always_that, "Banker")
bc = Baccarat(8, [ali])
bc.baccarat_simulator(20)
print(bc.overall_data)
'''