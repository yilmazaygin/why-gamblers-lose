import random

# Helper Functions (from newutils and newplayer)
def create_shoe(num_decks: int):
    """Create a shuffled shoe (deck of cards)."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    shoe = [f'{rank} of {suit}' for rank in ranks for suit in suits] * num_decks
    random.shuffle(shoe)
    return shoe

def shuffle_shoe(shoe):
    """Shuffle the shoe of cards."""
    random.shuffle(shoe)
    return shoe

def deal(shoe):
    """Deal a card from the shoe."""
    return shoe.pop()

# Blackjack Class
class BlackJack:
    def __init__(self): 
        self.dealers_hand = ['4 of Clubs', '10 of Hearts']
        self.shoe = create_shoe(1)
        self.shoe = shuffle_shoe(self.shoe)

    def blackjack_hand_value(self, hand) -> tuple:
        card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                    '7': 7, '8': 8, '9': 9, '10': 10,
                    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
        
        total_value = 0
        ace_count = 0
        for card in hand:
            rank = card.split(' ')[0]
            if rank == 'Ace':
                ace_count += 1
            total_value += card_values[rank]

        while total_value > 21 and ace_count > 0:
            total_value -= 10
            ace_count -= 1

        if total_value == 21:
            return 21

        if ace_count > 0 and total_value < 21:
            alternative_value = total_value - 10
            if alternative_value > 0 and alternative_value != total_value:
                return (alternative_value, total_value)

        return total_value

    def basic_strategy(self, hand: list, dealer_card: str) -> str:
        """Basic strategy for blackjack."""
        value = self.blackjack_hand_value(hand)
        dealer_rank = dealer_card.split(' ')[0]
        
        # If value is more than 21, return bust
        if isinstance(value, int) and value > 21:
            return 'Bust'
        
        # If value is 21 or more, stand
        if isinstance(value, int) and value >= 17:
            return 'Stand'
        
        # Otherwise, make decisions based on basic strategy
        if isinstance(value, tuple):
            value = value[1]
        
        if value in [19, 20, 21]:
            return 'Stand'
        if value in [17, 18]:
            return 'Stand' if dealer_rank in ['2', '7', '8'] else 'Hit'
        if value == 16:
            return 'Stand' if dealer_rank in ['2', '3', '4', '5', '6'] else 'Hit'
        if value == 15:
            return 'Stand' if dealer_rank in ['2', '3', '4', '5', '6'] else 'Hit'
        if value == 14:
            return 'Stand' if dealer_rank in ['2', '3', '4', '5', '6'] else 'Hit'
        if value == 13:
            return 'Stand' if dealer_rank in ['2', '3', '4', '5', '6'] else 'Hit'
        if value == 12:
            return 'Stand' if dealer_rank in ['4', '5', '6'] else 'Hit'
        if value == 11:
            return 'Double' if dealer_rank not in ['10', 'Jack', 'Queen', 'King', 'Ace'] else 'Hit'
        if value == 10:
            return 'Double' if dealer_rank not in ['10', 'Jack', 'Queen', 'King', 'Ace'] else 'Hit'
        if value == 9:
            return 'Double' if dealer_rank in ['3', '4', '5'] else 'Hit'
        return 'Hit'

    def dealer_play(self):
        while True:
            dealer_value = self.blackjack_hand_value(self.dealers_hand)
            
            # Eğer dealer'ın elinin değeri bir tuple ise, uygun olan değeri seç
            if isinstance(dealer_value, tuple):
                dealer_value = max(dealer_value)  # İki değerden en uygun olanı al (21'e yakın olan)
            
            if dealer_value >= 17:
                break
            
            self.dealers_hand.append(deal(self.shoe))  # Dealer kart çeker
        
        return dealer_value

# Player Class for Martingale Strategy
class BJPlayer:
    def __init__(self, balance: int, first_bet: int):
        self.balance = balance
        self.bets = [first_bet]  # Initial bet
        self.hands = [[]]  # One hand at the beginning

    def add_hand(self, hand):
        self.hands.append(hand)
        self.bets.append(self.bets[0])

    def reset_hands(self):
        self.hands = [[]]
        self.bets = [self.bets[0]]

    def update_balance(self, amount):
        self.balance += amount

    def martingale(self):
        """Martingale strategy: double the bet after a loss, reset after a win."""
        if self.balance <= 0:
            print("Player has no balance left.")
            return False
        if self.balance < self.bets[0]:
            print("Player cannot afford the starting bet.")
            return False
        return True

# Game Simulation
def simulate_blackjack():
    # Set up game
    player = BJPlayer(10000, 100)  # Starting with 10,000 balance and 100 initial bet
    game = BlackJack()
    num_rounds = 100  # Number of rounds to simulate
    round_results = []

    for _ in range(num_rounds):
        if not player.martingale():
            break  # Stop if player can't continue with the Martingale strategy

        # Reset hands and deal initial cards
        game.shoe = shuffle_shoe(create_shoe(1))  # Reset deck for each round
        game.dealers_hand = [deal(game.shoe), deal(game.shoe)]
        player.hands = [[deal(game.shoe), deal(game.shoe)]]  # Initial 2 cards for player

        # Play the round
        for hand_index, hand in enumerate(player.hands):
            print(f"Round {_ + 1}: Player's hand {hand_index + 1} starting cards: {hand}")
            action = game.basic_strategy(hand, game.dealers_hand[0])
            print(f"Player's hand {hand_index + 1} action: {action}")

            if action == 'Hit':
                hand.append(deal(game.shoe))
            elif action == 'Double':
                player.bets[hand_index] *= 2
                hand.append(deal(game.shoe))
            elif action == 'Bust':
                player.update_balance(-player.bets[hand_index])
            
            # Show updated hand after action
            print(f"Player's hand {hand_index + 1} after action: {hand}")
        
        # Dealer plays
        dealer_value = game.dealer_play()
        print(f"Dealer's hand: {game.dealers_hand} with value {dealer_value}")

        # Normalize dealer_value and player_value to get a single value (in case of a tuple)
        if isinstance(dealer_value, tuple):
            dealer_value = max(dealer_value)
        
        for hand_index, hand in enumerate(player.hands):
            player_value = game.blackjack_hand_value(hand)
            
            # Normalize player_value to get a single value (in case of a tuple)
            if isinstance(player_value, tuple):
                player_value = max(player_value)
            
            bet = player.bets[hand_index]

            if player_value > 21:
                print(f"Player's hand {hand_index + 1} is a bust. Lost {bet}")
                player.update_balance(-bet)
            elif dealer_value > 21 or player_value > dealer_value:
                print(f"Player's hand {hand_index + 1} wins. Gained {bet}")
                player.update_balance(bet)
            elif player_value == dealer_value:
                print(f"Player's hand {hand_index + 1} ties.")
            else:
                print(f"Dealer wins. Player loses {bet}")
                player.update_balance(-bet)

        round_results.append(player.balance)
        print(f"Player's current balance: {player.balance}\n")

    return round_results

# Run the simulation
simulate_blackjack()
