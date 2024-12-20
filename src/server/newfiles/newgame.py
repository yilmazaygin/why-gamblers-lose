class Game:
    def __init__(self, players: list, sim_times: int):
        """
        Initializes the Game class with the game type, players, and simulation times.

        Args:
            players (list): List of player objects.
            sim_times (int): Number of times the game will be simulated.
        """
    
        self.players = players
        self.sim_times = sim_times

        # The active players are the players who are still playing the game for the current simulation.
        self.active_players = players.copy()
        # The betted players are the players who have placed a bet in the current round.
        self.betted_players = [] 

    def get_bets(self):
        """
        Checks if a player can bet and adds them to the betted_players list, if not removes them from the active_players list.
        """
        # Empty the dict for the current round
        self.betted_players = []
        for player in self.active_players[:]:
            if player.place_bet(): # place_bet is a method in the player class, returns True if the player can bet, False otherwise.
                self.betted_players.append(player) 
            else:
                self.active_players.remove(player)

    def evaluate_bets(self, result: list): # result is the result of the game, format is game specific?
        """
        Evaluates the bets of betted_players, pays accordingly.
        """
        for player in self.betted_players:
            player_last_bet = player.simulations_bet_history[-1]
            if player_last_bet["Bet Place"] in result.values():
                player.current_balance += player_last_bet["Bet Amount"] * 2
                player_last_bet["Bet Condition"] = True
                player_last_bet["Balance After Bet"] = player.current_balance
            else:
                player_last_bet["Bet Condition"] = False  
                player_last_bet["Balance After Bet"] = player.current_balance      
            player_last_bet["Bet Outcome"] = result
    
    def reset_game(self):
        """
        Resets the game for the next simulation.
        """
        self.active_players = self.players.copy()
        self.betted_players = []

        for player in self.players: 
            player.reset_player()

    def calc_data(self):
        """
        Calculate the data of the game.
        Note that each player has player.overall_data, In this function we will combine them and return a single dictionary.
        It's not fully functional, you need to implement the logic for combining the data.
        It just calcs all players' additional data.
        """
        for player in self.players:
            player.overall_data["Simulation Times"] = self.sim_times
            player.calc_additional_overall_data()
        

    