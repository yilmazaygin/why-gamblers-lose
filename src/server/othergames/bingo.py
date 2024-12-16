import random
import Player, betamountstrats

class Bingo:
    def __init__(self, other_players: int, rounds_to_simulate: int, card_price: float, base_prize: float):
        self.other_players = other_players
        self.rounds_to_simulate = rounds_to_simulate
        self.card_price = card_price
        self.base_prize = base_prize
        self.balls = list(range(1, 76))
        
    def create_card(self):
        B = random.sample(range(1, 16), 5)
        I = random.sample(range(16, 31), 5)
        N = random.sample(range(31, 46), 4)
        N.insert(2, "X")
        G = random.sample(range(46, 61), 5)
        O = random.sample(range(61, 76), 5)
        card = [B, I, N, G, O]
        return card

    def draw_a_ball(self, active_pool):
        drawn_ball = random.choice(active_pool)
        active_pool.remove(drawn_ball)
        return drawn_ball

    def check_drawn_ball_in_card(self, card: list, drawn_ball: int):
        for i in range(5):
            if drawn_ball in card[i]:
                card[i][card[i].index(drawn_ball)] = "X"
        return card

    def check_card(self, card: list) -> bool:
        for i in range(5):
            if all(card[i][j] == "X" for j in range(5)) or all(card[j][i] == "X" for j in range(5)):
                return True
            
        if all(card[i][i] == "X" for i in range(5)) or all(card[i][4 - i] == "X" for i in range(5)):
            return True
        
        return False

    def print_card(self, card: list):
        print("+" + "-" * 21 + "+")
        print("|  B   I   N   G   O  |")
        print("+" + "-" * 21 + "+")
        
        for row in zip(*card):
            print("| " + "  ".join(f"{cell:>2}" if cell != "X" else " X" for cell in row) + "  |")
        
        print("+" + "-" * 21 + "+")
        print()

    def simulate_single_round(self, player: object):
        player_card = self.create_card()
        other_cards = [self.create_card() for _ in range(self.other_players)]
        active_pool = self.balls[:]
        prize_pool = self.base_prize
        
        print(f"Prize Pool for this round: ${prize_pool}")
        print("Your Card:")
        self.print_card(player_card)

        while True:
            drawn_ball = self.draw_a_ball(active_pool)
            print(f"Ball Drawn: {drawn_ball}")

            player_card = self.check_drawn_ball_in_card(player_card, drawn_ball)

            if self.check_card(player_card):
                print("\nCongratulations! You won the Bingo!")
                print("Your Winning Card:")
                self.print_card(player_card)
                return "Player", prize_pool

            for i, card in enumerate(other_cards):
                other_cards[i] = self.check_drawn_ball_in_card(card, drawn_ball)
                if self.check_card(other_cards[i]):
                    print(f"\nPlayer {i + 1} (other) wins the Bingo!")
                    print(f"Player {i + 1}'s Winning Card:")
                    self.print_card(other_cards[i])
                    return f"Other Player {i + 1}", prize_pool

            if not active_pool:
                print("\nNo more balls! Game ends in a draw.")
                return "Draw", 0

    def full_simulate_bingo(self, player: object):
        results = {"Player": 0, "Other Players": 0, "Draw": 0}
        total_prizes = 0

        for round_number in range(1, self.rounds_to_simulate + 1):
            print(f"\n--- Round {round_number} ---")
            winner, prize = self.simulate_single_round(player)
            
            if winner == "Player":
                results["Player"] += 1
            elif winner.startswith("Other Player"):
                results["Other Players"] += 1
            else:
                results["Draw"] += 1
            
            total_prizes += prize

        print("\n--- Simulation Results ---")
        print(f"Rounds Simulated: {self.rounds_to_simulate}")
        print(f"Player Wins: {results['Player']}")
        print(f"Other Players Wins: {results['Other Players']}")
        print(f"Draws: {results['Draw']}")
        print(f"Total Prize Money Distributed: ${total_prizes}")

# Simülasyon başlat
bg = Bingo(other_players=58, rounds_to_simulate=10, card_price=5, base_prize=50)
ali = Player.Player(500, 1, 550, 450, betamountstrats.martingale, None, None)
bg.full_simulate_bingo(ali)
