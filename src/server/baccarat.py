import random
import Player
import betamountstrats

class Baccarat: # Baccarat Class
    payrates = {"Player": 2, "Tie": 9, "Banker": 1.95}

    def __init__(self, deck_amount): # Constructor
        self.deck_amount = deck_amount
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

    def value_of_hand(self, hand): # Calculates the value of the hand, returns the value
        value = 0
        values = {"Ace":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":0, "Jack":0, "Queen":0, "King":0}
        for card in hand:
            card_value = card.split(" ")[0]
            value += values[card_value]
        return value % 10

    def player_play(self, hand_value): # Player Play Logic, returns True or False for hitting
        if hand_value in [0, 1, 2, 3, 4, 5]:
            return True
        elif hand_value in [6, 7, 8, 9]:
            return False

    def banker_play(self, hand_value, player_third_card=None): # Banker Play Logic, returns True or False for hitting
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

    def deal_hand(self, deck): # Deals the hand, returns the hand
        return [deck.pop(), deck.pop()]
        
    def baccarat_simulator(self, player): # Baccarat Simulator for one player, one time
        deck = self.deck_creator(8)
        deck = self.shuffle_deck(deck)

        print("Player Start Balance:", player.current_bal)
        game_condition = True
        
        while game_condition:
            if len(deck) <= 52:
                game_condition = False
                break

            can_player_bet = player.place_bet()  # Bet is already deducted here
            if not can_player_bet:
                game_condition = False
                break

            result = None
            player_hand = []
            banker_hand = []
            player_hand = self.deal_hand(deck)
            banker_hand = self.deal_hand(deck)

            player_value = self.value_of_hand(player_hand)
            banker_value = self.value_of_hand(banker_hand)
            
            if self.player_play(player_value):
                player_hand.append(deck.pop())
                player_value = self.value_of_hand(player_hand)

            if self.banker_play(banker_value, player_hand[-1] if len(player_hand) > 2 else None):
                banker_hand.append(deck.pop())
                banker_value = self.value_of_hand(banker_hand)

            if player_value > banker_value:
                result = "Player"
            elif banker_value > player_value:
                result = "Banker"
            else:
                result = "Tie"
            
            if player.bet_history[-1]["Bet Place"] == result:
                player.current_bal += player.bet_history[-1]["Bet Amount"] * Baccarat.payrates[result]
                player.bet_history[-1]["Bet Condition"] = True
            else:
                player.bet_history[-1]["Bet Condition"] = False

            self.game_history.append(result)

        self.simulation_history.append({"Simulation No": None,"Player's Starting Balance": player.starting_balance, "Player's Ending Balance": player.current_bal})
        print("Player's Ending Balance:", player.current_bal)
        
    def full_baccarat_simulator(self, player, simulation_times:int): # Full Baccarat Simulator for one player, multiple times
        for simulation in range(simulation_times):
            Baccarat.baccarat_simulator(self, player)
            self.simulation_history[simulation]["Simulation No"] = simulation + 1
            print(f"Simulation No:{simulation + 1} // Game History:", self.game_history) 
            for bet in player.bet_history: print(bet) 
            player.reset_player() # Resetting the player for the next simulation
            self.game_history = [] # Resetting the game history for the next simulation

    def random_player_or_banker(self):
        return random.choice(("Player","Banker"))

    def last_winner(self):
        if not self.game_history:
            return random.choice(("Player","Banker"))
        return self.game_history[-1]
            
bc = Baccarat(3)
ali = Player.Player(500, 10, 550, 450, betamountstrats.martingale, bc.last_winner, None)
bc.full_baccarat_simulator(ali, 1)
for sim in bc.simulation_history:
    print(sim)
