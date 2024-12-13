class Game:
    def __init__(self, players: list, game_type:str):
        self.game_type = game_type
        self.players = players
        self.active_players = players.copy()
        self.betted_players = []
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

        self.overall_data = {
            "Overall Data": {
                "Overall Rounds Played": 0,
                "Overall Wagered": 0,
                "Overall Hands Won by Players": 0,
                "Overall Hands Lost by Players": 0,
                "Overall Casino Profit": 0
            },
        }

    def calc_data(self):
        for player in self.players:
            player.player_game_data["Ending Balance"] = player.current_bal
            player.player_game_data["Profit"] = player.current_bal - player.starting_balance
            self.data["Game Data"]["Casino Profit"] += player.starting_balance - player.current_bal
            if player.current_bal > player.starting_balance:
                self.data["Player Data"]["Profited Player's Total Gain"] += player.current_bal - player.starting_balance

    def get_bets(self):
        self.betted_players = []
        for player in self.active_players[:]:
            if player.place_bet():
                self.betted_players.append(player)
                self.data["Game Data"]["Wagered"] += player.bet_history[-1]['Bet Amount']
                player.player_game_data["Rounds Played"] += 1
            else:
                self.active_players.remove(player)

    def reset_data(self):
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

    def evaluate_bets(self, spun_number: int): #IT ONLY DOUBLES; EDİT LATER
        results = self.num_properties(spun_number)
        for player in self.betted_players:
            if not player.bet_history:
                continue
            player_bet = player.bet_history[-1]
            bet_place = player_bet['Bet Place']
            if bet_place in results.values():
                winnings = player_bet['Bet Amount'] * 2
                player.current_bal += winnings
                self.data["Game Data"]["Hands Won by Players"] += 1
            else:
                self.data["Game Data"]["Hands Lost by Players"] += 1

    def print_results(self):
        for player in self.players:
            print(f"Player's Starting Balance: {player.starting_balance} - Player's Ending Balance: {player.current_bal}")
        for data in self.data:
            print(f"{data}:")
            for key, value in self.data[data].items():
                print(f"    {key}: {value}")