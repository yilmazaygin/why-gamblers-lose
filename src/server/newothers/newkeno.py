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
            "Cards With Profit": 0,  # Kazanç sağlayan kartlar (profit)
            "Cards With Money Back": 0,  # Sadece para iadesi alanlar (3 eşleşme)
            "Average Numbers Matched (For Winning Cards)": 0,
            "Average Winnings (For Winning Cards)": 0,
            "Average Winnings (For All Cards)": 0,
            "Total Winnings": 0,
            "Matched Numbers": {str(i): 0 for i in range(11)},
            "Profit Rate": 0,  # Toplam profit oranı
            "Money Back Rate": 0,  # Money back (3 eşleşme) oranı
        }

        for result in results:
            match_count, winnings = result
            data_dict["Matched Numbers"][str(match_count)] += 1  # Increment match count
            if winnings > 0:  # If winnings are greater than 0
                if winnings > 1:  # Profit
                    data_dict["Cards With Profit"] += 1
                elif winnings == 1:  # Money back
                    data_dict["Cards With Money Back"] += 1

                data_dict["Average Numbers Matched (For Winning Cards)"] += match_count
                data_dict["Average Winnings (For Winning Cards)"] += winnings
                data_dict["Total Winnings"] += winnings

        # Avoid division by zero
        total_winning_cards = data_dict["Cards With Profit"] + data_dict["Cards With Money Back"]
        if total_winning_cards > 0:
            data_dict["Average Numbers Matched (For Winning Cards)"] = round(
                data_dict["Average Numbers Matched (For Winning Cards)"] / total_winning_cards
            )
            data_dict["Average Winnings (For Winning Cards)"] = round(
                data_dict["Average Winnings (For Winning Cards)"] / total_winning_cards
            )

        data_dict["Average Winnings (For All Cards)"] = round(
            data_dict["Total Winnings"] / len(results)
        )

        # Calculate profit and money back rates
        data_dict["Profit Rate"] = round((data_dict["Cards With Profit"] / len(results)) * 100, 2)
        data_dict["Money Back Rate"] = round((data_dict["Cards With Money Back"] / len(results)) * 100, 2)

        return data_dict


# TEST
keno = Keno()
my_nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
try:
    results = keno.simulate_single_card(my_nums, 1000)
    for key, value in results.items():
        print(f"{key}: {value}")
except ValueError as e:
    print(e)
