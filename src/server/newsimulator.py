import Player
import RouletteTable
import time

class Simulator:
    def __init__(self, starting_bet, starting_balance, stop_win, stop_loss, strategy, bet_color, wheel_type, max_bet, min_bet, simulation_count, max_rounds):
        self.player = Player.Player(starting_balance, starting_bet, stop_win, stop_loss, strategy, bet_color)
        self.roulette_table = RouletteTable.RouletteTable(wheel_type,max_bet, min_bet)
        self.simulation_count = simulation_count  
        self.max_rounds = max_rounds

        self.wins = 0
        self.loses = 0
        self.ties = 0

        self.balances = []
    
    # returns a data structure that contains the results of the single simulation
    def once_simulate(self):
        i = 0

        # player retakes the starting balance
        self.player.current_bal = self.player.starting_bal
        self.player.bet_history = []
        

        min_balance = self.player.starting_bal
        max_balance = 0
        max_bet_amount = 0
        balance_dict = dict()

        while i < self.max_rounds:
            is_valid = self.player.place_bet(self.player.bet_color)
            if is_valid:
                spun_number = self.roulette_table.spin_the_wheel()
                spun_number_properties = self.roulette_table.check_spun_number_properties(spun_number)
                if self.player.bet_history[-1]["Bet Type"] == spun_number_properties["Color"]:
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
    

sim = Simulator(1, 500, 750, 0, "martingale", "Red", RouletteTable.european_wheel, 1000, 1, 5, 200)
all_data = sim.simualte_all()
for data in all_data:
    print(data)
print("Wins: ", sim.wins)
print("Loses: ", sim.loses)