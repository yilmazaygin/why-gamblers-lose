import random
import Player
import betamountstrats

class Roulette:
    european_wheel = (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)
    american_wheel = (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 37, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2)
    triplezero_wheel= (38, 0, 37, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)
    payrates = {"Straight":36, "Split":18, "Street":12, "Corner":9, "Five-Line":7, "Six-Line":6, "Column":3, "Dozen":3, "Red/Black":2, "Odd/Even":2, "Low/High":2, }

    def __init__(self, wheel_type):
        self.wheel_type = wheel_type
        self.game_history = []
        self.simulation_history = []

    def spin_the_wheel(self):
        return random.choice(self.wheel_type)
    
    def check_spun_number_properties(self, spun_number):
        properties = {'Number': None, 'Color': None, 'Odd/Even': None, 'Low/High': None, 'Column': None, 'Dozen': None}
        red_numbers = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)

        if spun_number in  (0, 37, 38):
            properties = {'Number': 0, 'Color': 'Green', 'Odd/Even': 'N/A', 'Low/High': 'N/A', 'Column': 'N/A', 'Dozen': 'N/A'}
            properties['Number'] = "00" if spun_number == 37 else properties['Number']
            properties['Number'] = "000" if spun_number == 38 else properties['Number']
            return properties

        properties['Number'] = spun_number
        properties['Color'] = 'Red' if spun_number in red_numbers else 'Black'
        properties['Odd/Even'] = 'Even' if spun_number % 2 == 0 else 'Odd'
        properties['Low/High'] = 'Low' if spun_number <= 18 else 'High'
        properties['Column'] = ['1st', '2nd', '3rd'][(spun_number - 1) % 3]

        if spun_number <= 12:
            properties['Dozen'] = '1st'
        elif spun_number <= 24:
            properties['Dozen'] = '2nd'
        else:
            properties['Dozen'] = '3rd'

        return properties

    def roulette_simulator(self, player):
        print("Player Start Balance:", player.current_bal)
        game_condition = True

        while game_condition:
            can_player_bet = player.place_bet()  # Bet is already deducted here
            if not can_player_bet:
                game_condition = False
                break
            
            num = self.spin_the_wheel()
            num_properties = self.check_spun_number_properties(num)

            if player.bet_history[-1]["Bet Place"] in num_properties.values():
                player.current_bal += player.bet_history[-1]["Bet Amount"] * 2 #!!!!Edit this line to reflect the payrate of the bet
                player.bet_history[-1]["Bet Condition"] = True
            else:
                player.bet_history[-1]["Bet Condition"] = False

            self.game_history.append(num_properties)

        self.simulation_history.append({"Simulation No": None,"Player's Starting Balance": player.starting_balance, "Player's Ending Balance": player.current_bal})
        print("Player's Ending Balance:", player.current_bal)
    
    def full_roulette_simulator(self, player, simulation_times:int):
        for simulation in range(simulation_times):
            Roulette.roulette_simulator(self, player)
            self.simulation_history[simulation]["Simulation No"] = simulation + 1
            print(f"Simulation No:{simulation + 1}")
            for game in self.game_history: print(game) 
            for bet in player.bet_history: print(bet) 
            player.reset_player() # Resetting the player for the next simulation
            self.game_history = [] # Resetting the game history for the next simulation
        
    def random_that(self, that:tuple):
        return random.choice(that) # that must be a tuple of the following: ("Red", "Black"), ("Even", "Odd"), ("Low", "High") ...
    
    def always_that(self, that:str):
        return that # that must be one of the following: "Red", "Black", "Even", "Odd", "Low", "High" ...

    def last_winner_attr(self, attr:str):
        if not self.game_history:
            return random.choice(("Red","Black"))
        return self.game_history[-1][attr]        

rt = Roulette(Roulette.european_wheel)
ali = Player.Player(500, 10, 550, 450, betamountstrats.martingale, rt.last_winner_attr, "Color")
rt.full_roulette_simulator(ali, 1)
for sim in rt.simulation_history:
    print(sim)
