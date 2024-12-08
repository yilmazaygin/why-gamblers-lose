import random
import Player, betamountstrats

class BlackJack:
    def __init__(self, deck_amount:int, other_player_amount:int, rules=None):
        self.deck_amount = deck_amount
        self.other_player_amount = other_player_amount # Number of other players in the game, 0 - 6 other players is the range

        self.simulation_history = []
        self.game_history = []
        self.running_count = 0
        self.true_count = 0

        default_rules = {
            "allow_split": True,
            "max_splits": 1,
            "double_after_split": True,
            "split_draw_limit": None,
            "dealer_hits_soft_17": True,
            "blackjack_payout": "3:2",
            "deck_penetration": 75, # add a random value for this later, the value should be between 65 and 85
            "surrender_allowed": True,
            "insurance_allowed": True,
        }

        self.rules = {**default_rules, **(rules or {})}

    def deck_creator(self, deck_amount:int):
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        deck = [rank + " of " + suit for suit in suits for rank in ranks]
        return deck * deck_amount

    def shuffle_deck(self, deck:list):
        random.shuffle(deck)
        return deck

    @staticmethod
    def value_of_hand(hand:list):
        values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 1}
        total = 0
        ace_count = 0

        for card in hand:
            rank = card.split()[0]
            total += values[rank]
            if rank == "Ace":
                ace_count += 1

        if ace_count == 0:
            return total
        elif total + 10 <= 21:
            return (total, total + 10)
        else:
            return total
    
    def blackjack_simulator(self, player):
        deck = self.deck_creator(self.deck_amount)
        deck = self.shuffle_deck(deck)

        print("Player Start Balance:", player.current_bal)
        game_condition = True

        while game_condition:
            if len(deck) <= (self.deck_amount * 52 * self.rules["deck_penetration"] // 100): # Calculate the deck penetration
                print("Deck penetration reached. Reshuffling deck.")
                deck = self.deck_creator(self.deck_amount)
                deck = self.shuffle_deck(deck)

            can_player_bet = player.place_bet()
            if not can_player_bet:
                print("Player can't bet anymore. Ending simulation.")
                break

            dealer_hand = []
            simulated_player_hand = []
            other_players_hands = [[] for _ in range(self.other_player_amount)]
            
            for _ in range(2):
                dealer_hand.append(deck.pop())
                simulated_player_hand.append(deck.pop())
                for player_hand in other_players_hands:
                    player_hand.append(deck.pop())

            print("Dealer Hand:", dealer_hand)
            print("Player Hand:", simulated_player_hand)
            for player in range(self.other_player_amount):
                print(f"Player {player + 1} Hand:", other_players_hands[player])
            
            game_condition = False

    def check_blackjack(self, hand: list):
        if len(hand) == 2 and self.value_of_hand(hand) == 21:
            return True
        return False
    
    def surrender(self):
        self.player.current_bal += self.player.bet_history[-1]["Bet Amount"] / 2
        pass

    def insurance(self):
        if self.dealer_hand[0].split()[0] == "Ace":
            pass

    def split(self):
        pass

    def double_down(self):
        self.player.current_bal -= self.player.bet_history[-1]["Bet Amount"]
        self.player.bet_history[-1]["Bet Amount"] = self.player.bet_history[-1]["Bet Amount"] * 2
    
    def player_play(self, hand: list, dealer_hand: list):
        action = self.basic_strategy(hand, dealer_hand)

        if action == "Hit":
            hand.append(self.deck.pop())
            self.player_play(hand, dealer_hand)
        elif action == "Stand":
            pass
        elif action == "Double":
            self.double_down()
            hand.append(self.deck.pop())
            pass
        elif action == "Split":
            self.split()
        elif action == "Surrender":
            self.surrender()
        elif action == "Insurance":
            self.insurance()
        
    
    def basic_strategy(self, hand: list, dealer_hand: list):
        def get_rank(card):
            return card.split()[0]
        
        player_ranks = [get_rank(card) for card in hand]
        dealer_rank = get_rank(dealer_hand[0])
        hand_value = self.value_of_hand(hand)

        if len(hand) == 2 and player_ranks[0] == player_ranks[1]: # Pairs, splitting hands
            rank = player_ranks[0]
            if rank == "Ace": return "Split"
            if rank == "10": return "Stand"
            if rank == "9":
                return "Stand" if dealer_rank in ["7", "10", "Ace"] else "Split"
            if rank == "8": return "Split"
            if rank == "7":
                return "Hit" if dealer_rank in ["8", "9", "10", "Ace"] else "Split"
            if rank == "6":
                return "Hit" if dealer_rank in ["7", "8", "9", "10", "Ace"] else "Split"
            if rank == "5":
                return "Hit" if dealer_rank in ["10", "Ace"] else "Double"
            if rank == "4":
                return "Split" if dealer_rank in ["5", "6"] else "Hit"
            if rank in ["2", "3"]:
                return "Hit" if dealer_rank in ["8", "9", "10", "Ace"] else "Split"

        if "Ace" in player_ranks: # Soft hands with an Ace
            if len(hand) > 2: # Soft hands with more than 2 cards
                pass # Implement this later
            other_card = player_ranks[0] if player_ranks[1] == "Ace" else player_ranks[1]
            
            if other_card in ["8", "9", "10"]: return "Stand"
            if other_card == "7":
                if dealer_rank in ["2", "7", "8"]: return "Stand"
                if dealer_rank in ["3", "4", "5", "6"]: return "Double"
                return "Hit"
            if other_card == "6":
                return "Double" if dealer_rank in ["3", "4", "5", "6"] else "Hit"
            if other_card in ["4", "5"]:
                return "Double" if dealer_rank in ["4", "5", "6"] else "Hit"
            if other_card in ["2", "3"]:
                return "Double" if dealer_rank in ["5", "6"] else "Hit"

        if hand_value >= 17: return "Stand" # Hard hands, no Ace
        if hand_value in [13, 14, 15, 16]:
            return "Stand" if dealer_rank in ["2", "3", "4", "5", "6"] else "Hit"
        if hand_value == 12:
            return "Stand" if dealer_rank in ["4", "5", "6"] else "Hit"
        if hand_value == 11:
            return "Double" if dealer_rank != "Ace" else "Hit"
        if hand_value == 10:
            return "Double" if dealer_rank not in ["10", "Ace"] else "Hit"
        if hand_value == 9:
            return "Double" if dealer_rank in ["3", "4", "5", "6"] else "Hit"

        return "Hit" # Default action


ali = Player.Player(1000, 10, 1050, 900, betamountstrats.flat_bet, None, None)
bj = BlackJack(6, 5)
bj.blackjack_simulator(ali)
