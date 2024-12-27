import random
import copy

class Bingo:
    """
    The Bingo class we need to implement. It has the following methods:

    - __init__(): Constructor method that initializes the Bingo game.
    - reset_pool(): Reset the active pool to the initial pool.
    - create_card(): Create a Bingo card.
    - draw_a_ball(): Draw a ball from the pool.
    - check_drawn_ball_in_card(card, drawn_ball): Check if the drawn ball is in the Bingo card, and mark it if it is.
    - check_card(card): Check if the Bingo card is completed or not.
    - print_card(card): Format and print the Bingo card.
    - average_rounds_to_complete_card(card, times): Calculate the average number of rounds to complete the card, for given number of simulations.
    """
    def __init__(self): # Constructor method that initializes the Bingo game.
        self.balls = list(range(1, 76))
        self.active_pool = self.balls.copy()
        self.player_amounts = {
            "Low": (20, 50),
            "Low-Medium": (51, 100),
            "Medium": (101, 200),
            "Medium-High": (201, 500),
            "High": (501, 1000),
            "Very High": (1001, 5000),
        }

        self.player_card = self.create_card() # EDIT THIS LATER
    
    def reset_pool(self) -> None:
        """
        Reset the active pool to the initial pool.
        """
        self.active_pool = self.balls.copy()

    def create_card(self) -> list:
        """
        Create a Bingo card.

        Returns:
            list: Bingo card
        """
        B = random.sample(range(1, 16), 5)
        I = random.sample(range(16, 31), 5)
        N = random.sample(range(31, 46), 4)
        N.insert(2, "X")
        G = random.sample(range(46, 61), 5)
        O = random.sample(range(61, 76), 5)
        card = [B, I, N, G, O]
        return card

    def draw_a_ball(self) -> int:
        """
        Draw a ball from the pool and remove it from the active pool.

        Returns:
            int: Drawn ball from the pool
        """
        drawn_ball = random.choice(self.active_pool)
        self.active_pool.remove(drawn_ball)
        return drawn_ball

    def check_drawn_ball_in_card(self, card: list, drawn_ball: int) -> None:
        """
        Check if the drawn ball is in the Bingo card, and mark it if it is.

        Args:
            card (list): Bingo card to be checked
            drawn_ball (int): Ball drawn from the pool
        """
        for i in range(5):
            if drawn_ball in card[i]:
                card[i][card[i].index(drawn_ball)] = "X"

    def check_card(self, card: list) -> bool:
        """
        Check if the Bingo card is completed or not.

        Args:
            card (list): Bingo card to be checked

        Returns:
            bool: True if the Bingo card is completed, False otherwise
        """
        for i in range(5):
            if all(card[i][j] == "X" for j in range(5)) or all(card[j][i] == "X" for j in range(5)):
                return True
        if all(card[i][i] == "X" for i in range(5)) or all(card[i][4 - i] == "X" for i in range(5)):
            return True
        return False

    def print_card(self, card: list) -> None:
        """
        Format and print the Bingo card.
        """
        print("+" + "-" * 21 + "+")
        print("|  B   I   N   G   O  |")
        print("+" + "-" * 21 + "+")
        for row in zip(*card):
            print("| " + "  ".join(f"{cell:>2}" if cell != "X" else " X" for cell in row) + "  |")
        print("+" + "-" * 21 + "+")
        print()

    def create_players(self, num_players: int) -> list:
        """
        Create players with their Bingo cards for the given number of players.

        Args:
            num_players (int): Number of players

        Returns:
            list: List of players with their Bingo cards
        """
        players = []
        for _ in range(num_players):
            players.append(self.create_card())
        return players
    
    def random_player_amount(self, range: str) -> int:
        """
        Return a random player amount from the given range.

        Args:
            range (str): Range of player amounts

        Returns:
            int: Random player amount
        """
        ran_player_amount = random.randint(self.player_amounts[range][0], self.player_amounts[range][1])
        return ran_player_amount
    
    def simulate_single_round(self, cards: list) -> bool:
        """
        For modulizing simulate method, simulate a single round of Bingo game, implement later.
        A round is completed when a player completes their card.

        Returns:
            bool: True if a round is completed, False otherwise
        """
        pass

    def simulate(self, cards: list, sim_times: int) -> int:
        """
        Simulate the Bingo game with the given cards, sim_times times.
        """
        cards.append(self.player_card)
        cards_save = copy.deepcopy(cards)
        metadata = []
        data = {
            "Sim Times": sim_times,
            "Total Cards Per Game": len(cards),
            "Average Rounds To Complete Card": 0,
            "Games Won By Player": 0,
            "Player Wins / Sims": 0,
        }

        for sim in range(sim_times):
            self.reset_pool()
            cards = copy.deepcopy(cards_save)
            game = True
            metadata.append(0)
            while game:
                metadata[-1] += 1
                drawn_ball = self.draw_a_ball()
                for card in cards:
                    self.check_drawn_ball_in_card(card, drawn_ball)
                    if self.check_card(card):
                        if card == cards[-1]:
                            data["Games Won By Player"] += 1
                        game = False

        data["Average Rounds To Complete Card"] = round((sum(metadata) / sim_times), 2)
        data["Player Wins / Sims"] = round((data["Games Won By Player"] / sim_times) * 100, 2)
        return data

# Test
bg = Bingo()
cardsasdas = bg.create_players(25)
print(bg.simulate(cardsasdas, 50))
