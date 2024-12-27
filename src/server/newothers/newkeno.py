import random

PAYRATES = {
    0: 0, 1: 0, 2: 0, 3: 1, 4: 5, 5: 15,
    6: 50, 7: 150, 8: 500, 9: 1000, 10: 5000
}


class Keno:
    """
    Keno game class

    Attributes:
        numbers: list of numbers from 1 to 80

    Methods:
        draw_numbers: randomly draw 20 numbers from the list of numbers
        select_numbers: validate selected numbers
        check_winnings: check the number of matching numbers and the winnings
    """

    def __init__(self):
        self.numbers = list(range(1, 81))

    def draw_numbers(self) -> set:
        """
        Draw 20 random numbers from the list of numbers

        Returns:
            set: drawn numbers
        """
        return set(random.sample(self.numbers, 20))

    def select_numbers(self, selected_numbers: set) -> bool:
        """
        Validate the selected numbers

        Args:
            selected_numbers (set): selected numbers

        Returns:
            bool: True if the selected numbers are valid, False otherwise
        """
        if len(selected_numbers) != 10:
            return False
        if any(number not in self.numbers for number in selected_numbers):
            return False
        return True

    def check_winnings(self, selected_numbers: set, drawn_numbers: set) -> tuple:
        """
        Check the number of matching numbers and the winnings

        Args:
            selected_numbers (set): selected numbers
            drawn_numbers (set): drawn numbers

        Returns:
            tuple: number of matching numbers and winnings
        """
        matching_numbers = selected_numbers.intersection(drawn_numbers)
        return len(matching_numbers), PAYRATES.get(len(matching_numbers), 0)

    def simulate_single_card(self, selected_numbers: set, sim_times: int) -> dict:
        """
        Simulate a single card

        Args:
            selected_numbers (set): selected numbers
            sim_times (int): number of simulations

        Returns:
            dict: formatted simulation results
        """
        if not self.select_numbers(selected_numbers):
            raise ValueError("Selected numbers are invalid. Please select 10 unique numbers between 1 and 80.")

        results = []

        for _ in range(sim_times):
            drawn_numbers = self.draw_numbers()
            results.append(self.check_winnings(selected_numbers, drawn_numbers))

        return self.format_results(results)

    def simulate_multiple_cards(self, cards: list, sim_times: int) -> dict:
        """
        Simulate multiple cards in a single draw

        Args:
            cards (list): list of sets, where each set is a card of 10 numbers
            sim_times (int): number of simulations

        Returns:
            dict: results for each card and total combined results
        """
        if not all(self.select_numbers(card) for card in cards):
            raise ValueError("One or more cards are invalid. Each card must have 10 unique numbers between 1 and 80.")

        overall_results = {
            "Total Sims": sim_times,
            "Cards": [],
            "Combined Results": {
                "Total Winnings": 0,
                "Cards With Profit": 0,
                "Cards With Money Back": 0,
                "Average Winnings (Per Card)": 0,
                "Matched Numbers": {str(i): 0 for i in range(11)}
            }
        }

        for card in cards:
            card_results = []
            for _ in range(sim_times):
                drawn_numbers = self.draw_numbers()
                card_results.append(self.check_winnings(card, drawn_numbers))

            formatted_card_results = self.format_results(card_results)
            overall_results["Cards"].append(formatted_card_results)

            # Combine results for all cards
            overall_results["Combined Results"]["Total Winnings"] += formatted_card_results["Total Winnings"]
            overall_results["Combined Results"]["Cards With Profit"] += formatted_card_results["Cards With Profit"]
            overall_results["Combined Results"]["Cards With Money Back"] += formatted_card_results["Cards With Money Back"]
            for key in formatted_card_results["Matched Numbers"]:
                overall_results["Combined Results"]["Matched Numbers"][key] += formatted_card_results["Matched Numbers"][key]

        # Calculate averages for combined results
        total_cards = len(cards) * sim_times
        overall_results["Combined Results"]["Average Winnings (Per Card)"] = round(
            overall_results["Combined Results"]["Total Winnings"] / total_cards, 2
        )

        return overall_results

    def format_results(self, results: list) -> dict:
        """
        Format the results

        Args:
            results (list): results

        Returns:
            dict: formatted results
        """
        data_dict = {
            "Total Sims": len(results),
            "Cards With Profit": 0,
            "Cards With Money Back": 0,
            "Total Winnings": 0,
            "Matched Numbers": {str(i): 0 for i in range(11)}
        }

        for result in results:
            match_count, winnings = result
            data_dict["Matched Numbers"][str(match_count)] += 1
            if winnings > 0:
                if winnings > 1:
                    data_dict["Cards With Profit"] += 1
                elif winnings == 1:
                    data_dict["Cards With Money Back"] += 1
                data_dict["Total Winnings"] += winnings

        return data_dict


# TEST
keno = Keno()
my_cards = [
    {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
    {11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
    {21, 22, 23, 24, 25, 26, 27, 28, 29, 30}
]

try:
    results = keno.simulate_multiple_cards(my_cards, 100)
    print("Combined Results:")
    for key, value in results["Combined Results"].items():
        print(f"{key}: {value}")

    print("\nIndividual Card Results:")
    for idx, card_result in enumerate(results["Cards"]):
        print(f"Card {idx + 1}:")
        for key, value in card_result.items():
            print(f"  {key}: {value}")
except ValueError as e:
    print(e)
