class Game:
    def __init__(self, players: list, sim_times: int, rules: dict):
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
        self.rules = rules

    def get_bets(self) -> None:
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

    def evaluate_bets(self, result: dict, payrates: dict) -> None: # result is the result of the game, format is game specific?
        """
        Evaluates the bets of betted_players, pays accordingly.
        Payrates changes according to the game type.
        """
        for player in self.betted_players:
            player_last_bet = player.simulations_bet_history[-1]
            if player_last_bet["Bet Place"] in result.values():
                player.current_balance += player_last_bet["Bet Amount"] * payrates[player_last_bet["Bet Place"]]
                player_last_bet["Bet Condition"] = True
                player_last_bet["Balance After Bet"] = player.current_balance
            else:
                player_last_bet["Bet Condition"] = False  
                player_last_bet["Balance After Bet"] = player.current_balance      
            player_last_bet["Bet Outcome"] = result
    
    def reset_game(self) -> None:
        """
        Resets the game for the next simulation.
        """
        self.active_players = self.players.copy()
        self.betted_players = []

        for player in self.players: 
            player.reset_player()

    def calc_player_additional_ov_data(self) -> None:
        """
        Calculates every players additional data
        """

        for player in self.players:
            player.overall_data["Simulation Times"] = self.sim_times
            player.calc_additional_overall_data()
        
    def check_sim_times(self) -> None:
        """
        Checks if the simulation times are valid, if not sets the simulation times to 1.
        """
        # If the simulation times are less than 1 or not an integer, set the simulation times to 1
        if self.sim_times < 1 or not isinstance(self.sim_times, int):
            self.sim_times = 1
            print("Invalid simulation times, setting the simulation times to 1.")
    
    def add_sim_no(self, sim_no: int) -> None:
        """
        Add simulation no to every player.
        """
        for player in self.players:
            player.simulation_data["Simulation No"] = sim_no

    def player_data_merger(self) -> dict:
        """
        Merges the player data to the master data.
        """
        super_overall_data = {
            "Simulation Times": self.sim_times,
            "Players": len(self.players),
            "Total Simulated Players Count": self.sim_times * len(self.players),
            "Total Rounds Played": 0,
            "Total Rounds Won": 0,
            "Total Rounds Lost": 0,
            "Total Deposit": 0,
            "Total Wager": 0,
            "Total Profit": 0,
            "Total Simulation Ended In Profit": 0,
            "Total Simulation Ended In Loss": 0,
            "Total Highest Balance": 0,
            "Total Lowest Balance": 0,
            "Total Highest Bet": 0,
            "Total Longest Win Streak": 0,
            "Total Longest Loss Streak": 0,
            "Total Loss Rate": 0,
        }

        for player in self.players:
                data = player.overall_data
                super_overall_data["Total Rounds Played"] += data["Overall Rounds Played"]
                super_overall_data["Total Rounds Won"] += data["Overall Rounds Won"]
                super_overall_data["Total Rounds Lost"] += data["Overall Rounds Lost"]
                super_overall_data["Total Deposit"] += data["Overall Deposit"]
                super_overall_data["Total Wager"] += data["Overall Wagered"]
                super_overall_data["Total Profit"] += data["Overall Profit"]
                super_overall_data["Total Simulation Ended In Profit"] += data["Simulations Ended In Profit"]
                super_overall_data["Total Simulation Ended In Loss"] += data["Simulations Ended In Loss"]
                super_overall_data["Total Highest Balance"] = max(data["Overall Highest Balance"], super_overall_data["Total Highest Balance"])
                super_overall_data["Total Lowest Balance"] = super_overall_data["Total Highest Balance"]
                super_overall_data["Total Lowest Balance"] = min(data["Overall Lowest Balance"], super_overall_data["Total Lowest Balance"])
                super_overall_data["Total Highest Bet"] = max(data["Overall Highest Bet"], super_overall_data["Total Highest Bet"])
                super_overall_data["Total Longest Win Streak"] = max(data["Overall Longest Win Streak"], super_overall_data["Total Longest Win Streak"])
                super_overall_data["Total Longest Loss Streak"] = max(data["Overall Longest Loss Streak"], super_overall_data["Total Longest Loss Streak"])
                super_overall_data["Total Loss Rate"] += data["Overall Loss Rate"]
        super_overall_data["Total Loss Rate"] = round((super_overall_data["Total Loss Rate"] / len(self.players)), 2)
        return super_overall_data
    
    
    def most_data_calc(self) -> dict:
        """
        Calculates the most data for the players.

        Returns:
            player_based_data (dict): The player based data
        """
        player_based_data = {
        "Played Most Rounds // Player": None,
        "Played Most Rounds // Amount": 0,
        
        "Biggest Wager // Player": None,
        "Biggest Wager // Amount": 0,

        "Highest Ending Balance // Player": None,
        "Highest Ending Balance // Amount": 0,

        "Biggest Bet // Player": None,
        "Biggest Bet // Amount": 0,

        "Longest Winning Streak // Player": None,
        "Longest Winning Streak // Amount": 0,

        "Longest Losing Streak // Player": None,
        "Longest Losing Streak // Amount": 0,
    }

        self.calc_player_additional_ov_data() # Calculate the additional overall data for every player.

        for player in self.players:
            for data in player.simulation_data_history:
                if data["Rounds Played"] > player_based_data["Played Most Rounds // Amount"]:
                    player_based_data["Played Most Rounds // Player"] = f"{player.player_id}-Sim:{data['Simulation No']}"
                    player_based_data["Played Most Rounds // Amount"] = data["Rounds Played"]

                if data["Wagered"] > player_based_data["Biggest Wager // Amount"]:
                    player_based_data["Biggest Wager // Player"] = f"{player.player_id}-Sim:{data['Simulation No']}"
                    player_based_data["Biggest Wager // Amount"] = data["Wagered"]

                if data["Balance After Simulation"] > player_based_data["Highest Ending Balance // Amount"]:
                    player_based_data["Highest Ending Balance // Player"] = f"{player.player_id}-Sim:{data['Simulation No']}"
                    player_based_data["Highest Ending Balance // Amount"] = data["Balance After Simulation"]

                if data["Highest Bet"] > player_based_data["Biggest Bet // Amount"]:
                    player_based_data["Biggest Bet // Player"] = f"{player.player_id}-Sim:{data['Simulation No']}"
                    player_based_data["Biggest Bet // Amount"] = data["Highest Bet"]

                if data["Longest Win Streak"] > player_based_data["Longest Winning Streak // Amount"]:
                    player_based_data["Longest Winning Streak // Player"] = f"{player.player_id}-Sim:{data['Simulation No']}"
                    player_based_data["Longest Winning Streak // Amount"] = data["Longest Win Streak"]

                if data["Longest Loss Streak"] > player_based_data["Longest Losing Streak // Amount"]:
                    player_based_data["Longest Losing Streak // Player"] = f"{player.player_id}-Sim:{data['Simulation No']}"
                    player_based_data["Longest Losing Streak // Amount"] = data["Longest Loss Streak"]

        return player_based_data
    
    def datamaster(self) -> tuple:
        """"
        Calls the necessary methods to calculate the data.

        Returns:
            player_based_data (dict): The player based data.
            merged_data (dict): The merged data.
        """
        player_based_data = self.most_data_calc()
        merged_data = self.player_data_merger() # Merge the player data to the master data.
        return player_based_data, merged_data

    def append_rules(self, rules: dict) -> None:
        """
        Appends the rules to the game.

        Args:
            rules (dict): The rules to be appended.
        """
        for player in self.players:
            player.rules = rules