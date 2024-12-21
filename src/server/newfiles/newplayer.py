from newbetamountstrats import BetAmountStrats, get_bet_amount_strat
from newlogics import RouletteLogics
from newlogics import roulette_logic_dict

class Player:
    def __init__(self, player_id, starting_balance: int, starting_bet: int, stop_win: int, stop_loss: int, bas, bps, bps_arg):
        """
        Initializes the Player class with strategies, balance, and limits.

        Args:
            starting_balance (int): Initial balance of the player.
            starting_bet (int): Initial bet amount.
            stop_win (int): Balance at which the player stops after winning.
            stop_loss (int): Balance at which the player stops after losing.
            bas (callable): Bet amount strategy function.
            bps (callable): Bet placement strategy function.
            bps_arg (any): Optional argument for the bet placement strategy.
        """
        self.player_id = player_id
        self.starting_balance = starting_balance
        self.starting_bet = starting_bet
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.bas = bas
        self.bps = bps
        self.bps_argument = bps_arg

        self.current_balance = starting_balance

        # Histories to track bets and simulations
        self.simulations_bet_history = []
        self.overall_bet_history = []
        self.simulation_data_history = [] # This is just for debbugging purposes, will delete later

        # Data specific to the current simulation
        self.simulation_data = {
            "Simulation No": 0,
            "Rounds Played": 0,
            "Rounds Won": 0,
            "Rounds Lost": 0,
            "Wagered": 0,
            "Balance After Simulation": 0,
            "Profit": 0,
            "Highest Balance Seen": self.starting_balance,
            "Lowest Balance Seen": self.starting_balance,
            "Highest Bet": 0,
            "Longest Win Streak": 0,
            "Longest Loss Streak": 0,
            "Bet History": self.simulations_bet_history
        }

        # Cumulative data across all simulations
        self.overall_data = {
            "Simulation Times": 0,
            "Overall Rounds Played": 0,
            "Overall Rounds Won": 0,
            "Overall Rounds Lost": 0,
            "Overall Deposit": 0, 
            "Overall Wagered": 0,
            "Overall Profit": 0,
            "Simulations Ended In Profit": 0,
            "Simulations Ended In Loss": 0,
            "Overall Highest Balance": 0,
            "Overall Lowest Balance": self.starting_balance,
            "Overall Highest Bet": 0,
            "Overall Longest Win Streak": 0,
            "Overall Longest Loss Streak": 0,
            "Overall Loss Rate": 0,
            "Average Simulation Lenght": 0,
            "Average Ending Balance": 0,
        }

    def place_bet(self):
        """
        Places a bet using the configured strategies and updates the player's balance.
        
        Returns:
            bool: True if the bet was placed successfully, False otherwise.
        """
        # Check stop loss condition
        if self.current_balance <= self.stop_loss:
            return False

        # Check stop win condition
        if self.current_balance >= self.stop_win:
            return False

        # Determine the next bet amount using the bet amount strategy
        player_bas = BetAmountStrats(self.current_balance, self.starting_bet, self.simulations_bet_history)
        next_bet_amount = get_bet_amount_strat(self.bas, player_bas)

        # Ensure the player has enough balance to place the bet
        if next_bet_amount > self.current_balance or next_bet_amount == 0:
            return False

        '''# Determine the bet placement using the bet placement strategy
        if self.bps_argument is None:
            next_bet_placement = self.bps()
        else:
            next_bet_placement = self.bps(self.bps_argument)'''
        next_bet_placement = self.bps_argument

        # Create a bet dictionary to store bet details
        bet = {
            "Bet Amount": next_bet_amount,
            "Bet Place": next_bet_placement,
            "Bet Outcome": None,  # To be updated after the result
            "Bet Condition": None,  # To be updated after the result
            "Balance Before Bet": self.current_balance,
            "Balance After Bet": 0,  # Will be updated with profit/loss, RETURNS 0 ALL THE TIME FOR NOW
        }

        self.simulation_data["Rounds Played"] += 1

        # Append the bet to the current simulation's bet history
        self.simulations_bet_history.append(bet)

        # Deduct the bet amount from the player's balance
        self.current_balance -= next_bet_amount

        return True

    def reset_player(self):
        """
        Resets the player state at the end of a simulation and updates overall data.
        """
        # Append the current simulation's bet history to overall bet history
        self.overall_bet_history.append(self.simulations_bet_history)
        self.calc_player_round_data()
        # Update overall statistics with current simulation data
        self.overall_data["Overall Rounds Played"] += self.simulation_data["Rounds Played"]
        self.overall_data["Overall Rounds Won"] += self.simulation_data["Rounds Won"]
        self.overall_data["Overall Rounds Lost"] += self.simulation_data["Rounds Lost"]
        self.overall_data["Overall Wagered"] += self.simulation_data["Wagered"]
        self.overall_data["Overall Profit"] += self.simulation_data["Profit"]
        self.overall_data["Overall Deposit"] += self.starting_balance

        # Check if the simulation ended in profit or loss
        if self.simulation_data["Profit"] > 0:
            self.overall_data["Simulations Ended In Profit"] += 1
        elif self.simulation_data["Profit"] < 0:
            self.overall_data["Simulations Ended In Loss"] += 1

        # Update overall highest and lowest balances
        self.overall_data["Overall Highest Balance"] = max(
            self.overall_data["Overall Highest Balance"],
            self.simulation_data["Highest Balance Seen"]
        )
        self.overall_data["Overall Lowest Balance"] = min(
            self.overall_data["Overall Lowest Balance"],
            self.simulation_data["Lowest Balance Seen"]
        )

        # Update overall highest bet
        self.overall_data["Overall Highest Bet"] = max(
            self.overall_data["Overall Highest Bet"],
            self.simulation_data["Highest Bet"]
        )

        # Update overall win and loss streaks
        self.overall_data["Overall Longest Win Streak"] = max(
            self.overall_data["Overall Longest Win Streak"],
            self.simulation_data["Longest Win Streak"]
        )
        self.overall_data["Overall Longest Loss Streak"] = max(
            self.overall_data["Overall Longest Loss Streak"],
            self.simulation_data["Longest Loss Streak"]
        )

        self.simulation_data["Balance After Simulation"] = self.current_balance
        self.simulation_data_history.append(self.simulation_data) # This is just for debbugging purposes, will delete later
        # Reset simulation-specific data for the next run
        self.simulations_bet_history = []
        self.simulation_data = {
            "Simulation No": self.simulation_data["Simulation No"] + 1,
            "Rounds Played": 0,
            "Rounds Won": 0,
            "Rounds Lost": 0,
            "Wagered": 0,
            "Balance After Simulation": 0,
            "Profit": 0,
            "Highest Balance Seen": self.starting_balance,
            "Lowest Balance Seen": self.starting_balance,
            "Highest Bet": 0,
            "Longest Win Streak": 0,
            "Longest Loss Streak": 0,
            "Bet History": self.simulations_bet_history
        }

        # Reset the player's balance for the next simulation
        self.current_balance = self.starting_balance

    def calc_player_round_data(self):
        """
        This method calculates the round data for the player, 
        including win and loss streaks.
        """
        current_win_streak = 0
        current_loss_streak = 0

        for bet in self.simulations_bet_history:
            # Update the wagered amount
            self.simulation_data["Wagered"] += bet["Bet Amount"]

            # Update the balance after the bet outcome
            if bet["Bet Condition"] == True:
                self.simulation_data["Rounds Won"] += 1
                current_win_streak += 1
                current_loss_streak = 0  # Reset loss streak
            else:
                self.simulation_data["Rounds Lost"] += 1
                current_loss_streak += 1
                current_win_streak = 0  # Reset win streak

            # Update the highest and lowest balance seen
            self.simulation_data["Highest Balance Seen"] = max(
                self.simulation_data["Highest Balance Seen"], bet["Balance After Bet"]
            )
            self.simulation_data["Lowest Balance Seen"] = min(
                self.simulation_data["Lowest Balance Seen"], bet["Balance After Bet"]
            )

            # Update the highest bet
            self.simulation_data["Highest Bet"] = max(
                self.simulation_data["Highest Bet"], bet["Bet Amount"]
            )

            # Update the longest win and loss streaks
            self.simulation_data["Longest Win Streak"] = max(
                self.simulation_data["Longest Win Streak"], current_win_streak
            )
            self.simulation_data["Longest Loss Streak"] = max(
                self.simulation_data["Longest Loss Streak"], current_loss_streak
            )

        # Calculate profit for the simulation
        self.simulation_data["Profit"] = self.current_balance - self.starting_balance


    def calc_additional_overall_data(self):
        """
        Calculates additional statistics such as loss rate for overall data.
        """
        total_rounds = self.overall_data["Overall Rounds Played"]
        total_losses = self.overall_data["Overall Rounds Lost"]

        # Calculate the overall loss rate
        if total_rounds > 0:
            self.overall_data["Overall Loss Rate"] = round((total_losses / total_rounds) * 100, 2)
        else:
            self.overall_data["Overall Loss Rate"] = 0

        # Calculate the average simulation length    
        self.overall_data["Average Simulation Lenght"] = round((self.overall_data["Overall Rounds Played"] / self.overall_data["Simulation Times"]), 1)
        self.overall_data["Average Ending Balance"] = round(((self.overall_data["Overall Deposit"] + self.overall_data["Overall Profit"]) / self.overall_data["Simulation Times"]), 2)

    def ov_data_printer(self):
        """
        Prints the overall data dict of the player line by line.
        """
        print("-------------------")
        for key, value in self.overall_data.items():
            print(f"{key}: {value}")
        print("-------------------")