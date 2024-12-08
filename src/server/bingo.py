import random
import Player, betamountstrats

class Bingo:
    def __init__(self, other_players: int):
        balls = list(range(1, 76))
        self.active_pool = balls
        self.other_players = other_players

    def create_card(self):
        B = random.sample(range(1, 16), 5)
        I = random.sample(range(16, 31), 5)
        N = random.sample(range(31, 46), 4)
        N.insert(2, "X")
        G = random.sample(range(46, 61), 5)
        O = random.sample(range(61, 76), 5)
        card = [B, I, N, G, O]
        return card

    def draw_a_ball(self):
        drawn_ball = random.choice(self.active_pool)
        self.active_pool.remove(drawn_ball)
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

    def print_card(self, card):
        print("+" + "-" * 21 + "+")
        print("|  B   I   N   G   O  |")
        print("+" + "-" * 21 + "+")
        
        for row in zip(*card):
            print("| " + "  ".join(f"{cell:>2}" if cell != "X" else " X" for cell in row) + "  |")
        
        print("+" + "-" * 21 + "+")
        print()

    def simulate_bingo(self, player: object):
        player_card = self.create_card()
        other_cards = [self.create_card() for _ in range(self.other_players)]
        
        print("Your Card:")
        self.print_card(player_card)

        for i, card in enumerate(other_cards):
            print(f"Player {i + 1}:")
            self.print_card(card)

        while True:
            drawn_ball = self.draw_a_ball()
            print(f"Ball Drawn: {drawn_ball}")

            player_card = self.check_drawn_ball_in_card(player_card, drawn_ball)

            if self.check_card(player_card):
                print("\nCongratulations! You won the Bingo!")
                print("Your Card:")
                self.print_card(player_card)
                break

            for i, card in enumerate(other_cards):
                other_cards[i] = self.check_drawn_ball_in_card(card, drawn_ball)
                if self.check_card(other_cards[i]):
                    print(f"\nPlayer {i + 1} (other) wins the Bingo!")
                    print(f"Player {i + 1}'s card:")
                    self.print_card(other_cards[i])
                    return

            if not self.active_pool:
                print("\nNo more balls! Game ends in a draw.")
                break


bg = Bingo(2)
ali = Player.Player(500, 1, 550, 450, betamountstrats.martingale, None, None)
bg.simulate_bingo(ali)
