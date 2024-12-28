import random
# Payrates for each amount of spots
TEN_SPOTS = {"0": 4, "1": 0, "2": 0, "3": 0, "4": 0, "5": 2, "6": 10, "7": 50, "8": 400, "9": 4000, "10": 100000}
NINE_SPOTS = {"0": 2, "1": 0, "2": 0, "3": 0, "4": 0, "5": 5, "6": 20, "7": 100, "8": 2500, "9": 25000}
EIGHT_SPOTS = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 2, "5": 10, "6": 50, "7": 500, "8": 10000}
SEVEN_SPOTS = {"0": 0, "1": 0, "2": 0, "3": 1, "4": 3, "5": 15, "6": 100, "7": 2500}
SIX_SPOTS = {"0": 0, "1": 0, "2": 0, "3": 1, "4": 5, "5": 50, "6": 1000}
FIVE_SPOTS = {"0": 0, "1": 0, "2": 0, "3": 2, "4": 15, "5": 300}
FOUR_SPOTS = {"0": 0, "1": 0, "2": 1, "3": 5, "4": 50}
THREE_SPOTS = {"0": 0, "1": 0, "2": 2, "3": 25}
TWO_SPOTS = {"0": 0, "1": 0, "2": 10}
ONE_SPOT = {"0": 0, "1": 2}

def get_payrates(spots: int) -> dict:
    """
    Returns the payrates for the amount of spots given

    Args:
        spots (int): The amount of spots

    Returns:
        dict: The payrates for the amount of spots given
    """
    if spots == 10: return TEN_SPOTS
    elif spots == 9: return NINE_SPOTS
    elif spots == 8: return EIGHT_SPOTS
    elif spots == 7: return SEVEN_SPOTS
    elif spots == 6: return SIX_SPOTS
    elif spots == 5: return FIVE_SPOTS
    elif spots == 4: return FOUR_SPOTS
    elif spots == 3: return THREE_SPOTS
    elif spots == 2: return TWO_SPOTS
    elif spots == 1: return ONE_SPOT
    else:
        raise ValueError("Invalid amount of spots")

class KenoCard:
    """
    Class for a Keno card.

    Args:
        nums (set): The numbers on the
    
    Attributes:
        numbers (list): The numbers on the card
        payrates (dict): The payrates for the card
        card_history (list): The history of the card
        card_data (dict): The data of the card

    Methods:
        calc_card_data: Calculates the data of the card
    """
    def __init__(self, nums: set): # Constructor
        self.numbers = sorted(nums)
        self.payrates = get_payrates(len(nums))
        self.card_history = []
        self.card_data = {
            "Numbers": sorted(self.numbers),
            "Matches": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0},
            "Sims Played": 0,
            "Biggest Match": 0,
            "Total Profit": 0,
        }

    def calc_card_data(self) -> None:
        """
        Calculates the data of the card
        """
        self.card_data["Sims Played"] = sum(self.card_data["Matches"].values())
        total_profit = 0
        i = 0
        for matches, sims in self.card_data["Matches"].items():
            if len(self.numbers) < i:
                break
            i+=1
            total_profit += sims * self.payrates[matches]
        self.card_data["Total Profit"] = total_profit - self.card_data["Sims Played"]
        self.card_data["Biggest Match"] = max(
            (key for key, value in self.card_data["Matches"].items() if value != 0),
            default=None
        )

class Keno:
    """
    Class for a Keno game.

    Methods:
        draw_numbers: Draws 20 random numbers
        get_matches: Gets the matches of a card
        calc_cards: Calculates the data of the cards
        simulate_keno: Simulates a game of Keno
    """
    def __init__(self):
        pass

    def draw_numbers(self) -> set:
        """
        Draws 20 random numbers from 1 to 80
        """
        return sorted(set(random.sample(range(1, 81), 20)))
    
    def get_matches(self, card: tuple, drawn_numbers: set) -> set:
        """
        Gets the matches of a card

        Args:
            card (tuple): The card
            drawn_numbers (set): The drawn numbers
        
        Returns:
            set: The matching numbers
        """
        matching_numbers = set(card.numbers).intersection(set(drawn_numbers))
        return matching_numbers

    def calc_cards(self) -> None:
        """
        Calculates the data of the cards
        """
        for card in cards:
            card.calc_card_data()

    def print_cards(self) -> None:
        """
        Prints the data of the cards
        """
        for card in cards:
            print(card.card_data)   

    def simulate_keno(self, cards: list[set], sim_times: int) -> dict:
        """
        Simulates a game of Keno

        Args:
            cards (list): The cards
            sim_times (int): The amount of simulations

        Returns:
            dict: The total data of the cards
        """
        for _ in range(sim_times):
            drawn_numbers = self.draw_numbers()
            for card in cards:
                matches = self.get_matches(card, drawn_numbers)
                card.card_data["Matches"][str(len(matches))] += 1
                card.card_history.append(matches)
        self.calc_cards()
        self.print_cards()
        return(self.total_data(cards))


    def total_data(self, cards: list[set]) -> dict:
        """
        Collects the total data of the cards

        Args:
            cards (list): The cards

        Returns:
            dict: The total data of the cards
        """
        total_data = {
            "Total Cards": len(cards),
            "Total Draws": 0,
            "Total Matches": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0},
            "Total Wagered": 0,
            "Total Profit": 0,
            "Biggest Match": 0,
        }
        for card in cards:
            total_data["Total Draws"] += card.card_data["Sims Played"]
            total_data["Total Wagered"] += card.card_data["Sims Played"]
            total_data["Total Profit"] += card.card_data["Total Profit"]
            for matches, sims in card.card_data["Matches"].items():
                total_data["Total Matches"][matches] += sims
            total_data["Biggest Match"] = max(int(total_data["Biggest Match"]), int(card.card_data["Biggest Match"]))

        return total_data

card1 = KenoCard({1})
card2 = KenoCard({1, 2})
card3 = KenoCard({1, 2, 3})
card4 = KenoCard({1, 2, 3, 4})
card5 = KenoCard({1, 2, 3, 4, 5})
card6 = KenoCard({1, 2, 3, 4, 5, 6})
card7 = KenoCard({1, 2, 3, 4, 5, 6, 7})
card8 = KenoCard({1, 2, 3, 4, 5, 6, 7, 8})
card9 = KenoCard({1, 2, 3, 4, 5, 6, 7, 8, 9})
card10 = KenoCard({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})

cards = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]
keno = Keno()
new_cards = [card10]
print(keno.simulate_keno(new_cards, 100000))