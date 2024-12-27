import random
# 5539745628 ZENEBİM

class KenoCard:
    def __init__(self, nums: set):
        self.numbers = sorted(nums)
        self.card_data = {
            "Numbers": sorted(self.numbers),
            "Matches": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0},
        }

    def additional_data(self):
        additional_data = {
            "Sims Played": sum(self.card_data["Matches"].values()),
            "Most Matched Amount": max(self.card_data["Matches"], key=self.card_data["Matches"].get),
        }

        return additional_data

class Keno:
    def __init__(self, spots: int):
        self.spots = spots

    def check_cards(self, card: KenoCard):
        for card in cards:
            if len(card.numbers) != self.spots:
                raise ValueError("Card does not have the correct amount of spots")

    def draw_numbers(self):
        return sorted(set(random.sample(range(1, 81), self.spots)))
    
    def get_matches(self, card: tuple, drawn_numbers: set):
        matching_numbers = set(card.numbers).intersection(set(drawn_numbers))
        return matching_numbers
    
    def calc_payout(self):
        pass

    def simulate_keno(self, cards: list[set], sim_times: int):
        self.check_cards(cards)
        for _ in range(sim_times):
            drawn_numbers = self.draw_numbers()
            for card in cards:
                matches = self.get_matches(card, drawn_numbers)
                card.card_data["Matches"][str(len(matches))] += 1


card1 = KenoCard({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
card2 = KenoCard({11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
card3 = KenoCard({21, 22, 23, 24, 25, 26, 27, 28, 29, 30})
cards = [card1, card2, card3]
keno = Keno(10)
keno.simulate_keno(cards, 1000)
print(card1.card_data)
print(card2.card_data)
print(card3.card_data)
