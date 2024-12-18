import utils
import random

class Game: # Game Class, contains the game data and player data. We will inherit this class to create different games.
    def __init__(self, players: list, game_type:str, sim_times: int): # Initializes the game
        self.game_type = game_type
        self.players = players
        self.sim_times =  sim_times
        self.active_players = players.copy()
        self.betted_players = []
        self.data_history = []
        self.new_data = {}
        self.data = {
            "Game Data": { # Game Data, will be used to store the game data of the game.
                "Rounds Played": 0,
                "Wagered": 0,
                "Hands Won by Players": 0,
                "Hands Lost by Players": 0,
                "Casino Profit": 0
            },
            "Player Data": {
                "Profited Players": 0,
                "Lost Players": 0,
                "Profited Player's Total Gain": 0
            },
        }

        self.overall_data = { # Overall Data, will be used to store the overall data of the game.
            "Overall Data": {
                "Overall Rounds Played": 0,
                "Overall Wagered": 0,
                "Overall Hands Won by Players": 0,
                "Overall Hands Lost by Players": 0,
                "Overall Casino Profit": 0
            },
            "Overall Player Data": {
                "Overall Profited Players": 0,
                "Overall Lost Players": 0,
                "Overall Profited Player's Total Gain": 0
            }
        }

    def calc_data(self): # Calculates the data of the game
        for player in self.players:
            player.player_game_data["Ending Balance"] = player.current_bal
            player.player_game_data["Profit"] = player.current_bal - player.starting_balance
            self.data["Game Data"]["Casino Profit"] += player.starting_balance - player.current_bal
            if player.current_bal > player.starting_balance:
                self.data["Player Data"]["Profited Players"] += 1
            else:
                self.data["Player Data"]["Lost Players"] += 1
            if player.current_bal > player.starting_balance:
                self.data["Player Data"]["Profited Player's Total Gain"] += player.current_bal - player.starting_balance

    def get_bets(self): # Gets the bets of the players
        self.betted_players = []
        for player in self.active_players[:]:
            if player.place_bet():
                self.betted_players.append(player)
                self.data["Game Data"]["Wagered"] += player.bet_history[-1]['Bet Amount']
                player.player_game_data["Rounds Played"] += 1
            else:
                self.active_players.remove(player)

    def reset_data(self): # Resets the data of the game
        self.data_history.append(self.data)
        self.data = {
            "Game Data": {
                "Rounds Played": 0,
                "Wagered": 0,
                "Hands Won by Players": 0,
                "Hands Lost by Players": 0,
                "Casino Profit": 0
            },
            "Player Data": {
                "Profited Players": 0,
                "Lost Players": 0,
                "Profited Player's Total Gain": 0
            },
        }

        for player in self.players:
            player.reset_player()
        
        self.active_players = self.players.copy()

    def print_results(self): # Prints the results of the game
        for player in self.players:
            print(f"Player's Starting Balance: {player.starting_balance} - Player's Ending Balance: {player.current_bal}")
        for data in self.data:
            print(f"{data}:")
            for key, value in self.data[data].items():
                print(f"    {key}: {value}")

    def evaluate_bets_list(self, result: list): # Evaluates the bets of the players, if the result is a list
        for player in self.betted_players:
            if not player.bet_history:
                continue
            player_bet = player.bet_history[-1]
            bet_place = player_bet['Bet Place']
            if bet_place in result.values():
                winnings = player_bet['Bet Amount'] * utils.payrates[self.game_type][bet_place]
                player.current_bal += winnings
                self.data["Game Data"]["Hands Won by Players"] += 1
                player_bet["Bet Condition"] = True
            else:
                self.data["Game Data"]["Hands Lost by Players"] += 1
                player_bet["Bet Condition"] = False

    def evaluate_bets_str(self, result: str): # Evaluates the bets of the players, if the result is a string
        for player in self.betted_players:
            if not player.bet_history:
                continue
            player_bet = player.bet_history[-1]
            bet_place = player_bet['Bet Place']
            if bet_place == result:
                winnings = player_bet['Bet Amount'] * utils.payrates[self.game_type][bet_place]
                player.current_bal += winnings
                self.data["Game Data"]["Hands Won by Players"] += 1
                player_bet["Bet Condition"] = True
            else:
                self.data["Game Data"]["Hands Lost by Players"] += 1
                player_bet["Bet Condition"] = False

    def deal(self, deck: list, card_receivers: list, times: int): # Deals the cards to the card_receivers, times times
        for _ in range(times):
            for receiver in card_receivers:
                receiver.append(deck.pop())

    def deck_creator(self, deck_amount: int): # Deck Creator, returns the deck_amount times the deck
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        deck = [rank + " of " + suit for suit in suits for rank in ranks]
        deck = deck * deck_amount
        return deck

    def shuffle_deck(self, deck: list): # Shuffles the Deck, returns the shuffled deck
        random.shuffle(deck)
        return deck
    
    def add_to_overall_data(self):
        for key, value in self.data["Game Data"].items():
            self.overall_data["Overall Data"][f"Overall {key}"] += value
        for key, value in self.data["Player Data"].items():
            self.overall_data["Overall Player Data"][f"Overall {key}"] += value
        
    def last_data(self):
        self.new_data = {
            "Total Different Players Simulated": len(self.players) * self.sim_times,
            "Lost Players Percentage": f"%{(self.overall_data['Overall Player Data']['Overall Lost Players'] / (len(self.players) * self.sim_times) * 100):.1f}",  # % formatı
            "Average Rounds Per Game": self.overall_data["Overall Data"]["Overall Rounds Played"] / self.sim_times,
        }
        return self.new_data
