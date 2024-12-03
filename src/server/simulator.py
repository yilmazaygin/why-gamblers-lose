import Player
import RouletteTable
import time

european_wheel = (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)
american_wheel = (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 37, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2)
triplezero_wheel= (38, 0, 37, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)


class Simulator:
    def __init__(self, starting_bet, starting_balance, stop_win, stop_loss, strategy, bet_color, wheel_type, max_bet, min_bet, simulation_count, max_rounds):
        self.player = Player.Player(starting_balance, starting_bet, stop_win, stop_loss, strategy, bet_color)
        if wheel_type == "european":
            self.roulette_table = RouletteTable.RouletteTable(european_wheel, max_bet, min_bet)
        elif wheel_type == "american":
            self.roulette_table = RouletteTable.RouletteTable(american_wheel, max_bet, min_bet)
        elif wheel_type == "triplezero":
            self.roulette_table = RouletteTable.RouletteTable(triplezero_wheel, max_bet, min_bet)
        
        self.simulation_count = simulation_count  
        self.max_rounds = max_rounds

        self.wins = 0
        self.loses = 0
        self.ties = 0

        self.balances = []
    
    # returns a data structure that contains the results of the single simulation
    def once_simulate(self):


        # player retakes the starting balance
        self.player.current_bal = self.player.starting_bal
        self.player.bet_history = []
        

        min_balance = self.player.starting_bal
        max_balance = 0
        max_bet_amount = 0
        balance_dict = dict()
        print(balance_dict)
        i = 0
        while i < self.max_rounds:
            is_valid = self.player.place_bet(self.player.bet_color)
            if is_valid:
                spun_number = self.roulette_table.spin_the_wheel()
                spun_number_properties = self.roulette_table.check_spun_number_properties(spun_number)
                if self.player.bet_history[-1]["Bet Type"] == spun_number_properties["Color"].lower():
                    self.player.current_bal += self.player.bet_history[-1]["Bet Amount"]
                    self.player.bet_history[-1]["Bet Condition"] = True
                else:
                    self.player.current_bal -= self.player.bet_history[-1]["Bet Amount"]
                    self.player.bet_history[-1]["Bet Condition"] = False

                if self.player.current_bal > max_balance:
                    max_balance = self.player.current_bal
                
                if self.player.current_bal < min_balance:
                    min_balance = self.player.current_bal

                if self.player.bet_history[-1]["Bet Amount"] > max_bet_amount:
                    max_bet_amount = self.player.bet_history[-1]["Bet Amount"]
            else:
                break

            i += 1
        
        balance_dict["end_balance"] = self.player.current_bal
        balance_dict["max_balance"] = max_balance
        balance_dict["min_balance"] = min_balance
        balance_dict["max_bet_amount"] = max_bet_amount
        print(balance_dict)
        self.balances.append(balance_dict)

        if self.player.current_bal > self.player.starting_bal:
            self.wins += 1
        elif self.player.current_bal < self.player.starting_bal:
            self.loses += 1
        else:
            self.ties += 1

    def simualte_all(self):
        for i in range(self.simulation_count):
            self.once_simulate()
        return self.balances


sim = Simulator(10, 1000, 2000, 100, "martingale", "Red", None, 100, 10, 100, 1000)