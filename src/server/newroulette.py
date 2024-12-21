from newgame import Game
import random

EUROPEAN_WHEEL = (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)
AMERICAN_WHEEL = (0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 37, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2)
TRIPLEZERO_WHEEL = (38, 0, 37, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)

ROULETTE_PAYRATES = {
    "Red": 2, "Black": 2,
    "Odd": 2, "Even": 2,
    "High": 2, "Low": 2,
    "1st Column": 3, "2nd Column": 3, "3rd Column": 3,
    "1st Dozen": 3, "2nd Dozen": 3, "3rd Dozen": 3,
}

class Roulette(Game):
    def __init__(self, players: list, sim_times: int, rules: dict, wheel: str,):
        """
        Initializes the Roulette class with the players, simulation times, rules, and wheel.

        Args:
            players (list): List of player objects.
            sim_times (int): Number of times the game will be simulated.
            wheel (tuple): Tuple of the wheel numbers
            rules (dict): Dictionary of the rules of the game, such as min or max bet amount.
        """
        super().__init__(players, sim_times, rules) # Inherit from Game class
        self.wheel = wheel 

    def check_wheel(self) -> None:
        """
        Checks if the wheel is valid, if not sets the wheel to European Wheel.
        """
        # If the wheel is not one of the predefined wheels, set the wheel to European Wheel
        if self.wheel not in ("EUROPEAN_WHEEL", "AMERICAN_WHEEL", "TRIPLEZERO_WHEEL"):
            self.wheel = EUROPEAN_WHEEL
            print("Invalid wheel, setting the wheel to European Wheel.")
        else:
            self.wheel = globals()[self.wheel] # Get the wheel from the globals

    def spin_wheel(self) -> int:
        """
        Returns a random number from the wheel.
        """
        number = random.choice(self.wheel)
        return number

    def num_properties(self, spun_number: int) -> dict:
        """
        Returns the properties of the spun number.

        Args:
            spun_number (int): The spun number.

        Returns:
            dict: The properties of the spun number.

        Note that 37 is 00 and 38 is 000
        """
        # Properties of the spun number are stored in a dictionary, we will return this dictionary after setting the properties
        properties = {
            'Number': None,
            'Color': None,
            'Odd/Even': None,
            'Low/High': None,
            'Column': None,
            'Dozen': None
        }
        red_numbers = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36) # Red numbers are same for each wheel

        # If the spun number is 0, 00, or 000, the properties are set accordingly
        if spun_number in (0, 37, 38):
            properties = {
                'Number': "0" if spun_number == 0 else "00" if spun_number == 37 else "000",
                'Color': 'Green',
                'Odd/Even': 'N/A',
                'Low/High': 'N/A',
                'Column': 'N/A',
                'Dozen': 'N/A'
            }
            return properties

        properties['Number'] = spun_number
        properties['Color'] = 'Red' if spun_number in red_numbers else 'Black'
        properties['Odd/Even'] = 'Even' if spun_number % 2 == 0 else 'Odd'
        properties['Low/High'] = 'Low' if spun_number <= 18 else 'High'
        properties['Column'] = ['1st Column', '2nd Column', '3rd Column'][(spun_number - 1) % 3]

        if spun_number <= 12:
            properties['Dozen'] = '1st Dozen'
        elif spun_number <= 24:
            properties['Dozen'] = '2nd Dozen'
        else:
            properties['Dozen'] = '3rd Dozen'

        return properties

    def roulette_simulator(self) -> None:
        """
        Simulates the roulette game, will run sim_times times.
        Each player will reset themself after each simulation.
        The game will reset itself after each simulation.

        """
        self.check_wheel()
        self.check_sim_times()
        self.append_rules(self.rules)
        
        for _ in range(self.sim_times): # Loop through the number of simulations
            sim_no = (_ + 1)
            self.add_sim_no(sim_no)
            while self.active_players: # While there are active players
                self.get_bets()
                if not self.active_players: # If there are no active players, break the loop
                    break
                spun_number = self.spin_wheel()
                spun_number_properties = self.num_properties(spun_number)

                self.evaluate_bets(spun_number_properties, ROULETTE_PAYRATES) # Evaluate the bets according to the spun number properties
            self.reset_game()

        self.datamaster()
        