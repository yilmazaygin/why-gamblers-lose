from newutils import create_shoe, shuffle_shoe, deal, reset_hands
from newplayer import Player

class BlackJack:
    """
    Blackjack class. WILL EDIT THIS LATER.
    """
    def __init__(self): # Constructor
        self.dealers_hand = ['4 of Clubs', '10 of Hearts']
        self.shoe = create_shoe(1)
        self.shoe = shuffle_shoe(self.shoe)

    def blackjack_hand_value(self, hand) -> tuple:
        """
        Calculates the value of a blackjack hand.
        Args:
            hand (list): A list of strings representing the cards in the hand (e.g., 'Ace of Clubs', '2 of Hearts').
        
        Returns:
            int: The value of the hand. If the hand contains an ace, this will be the highest possible value without going over 21. 
            If the hand contains more than one ace, only one ace can have the value of 11, and this will be reduced to 1 if the hand would otherwise bust.
            tuple: If the hand contains an ace, this will be a tuple of two integers. The first integer is the value of the hand with the ace valued as 1, and the second integer is the value of the hand with the ace valued as 11.
        """
        card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                    '7': 7, '8': 8, '9': 9, '10': 10,
                    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
        
        total_value = 0
        ace_count = 0

        # Loop through each card in the hand
        for card in hand:
            # Extract the rank (the first part of the card string before 'of')
            rank = card.split(' ')[0]

            # Count aces and add card values
            if rank == 'Ace':
                ace_count += 1
            total_value += card_values[rank]

        # Adjust for aces if total value exceeds 21
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

    def pairs(self, hand: list):
        """
        If the hand contains a pair, this function will return the recommended action based on the basic strategy.

        Args:
            hand (list): A list of strings representing the cards in the hand (e.g., 'Ace of Clubs', '2 of Hearts').

        Returns:
            str: The recommended action based on the basic strategy. One of 'Hit', 'Stand', 'Double', 'Split'.
        """
        if len(hand) != 2 or hand[0].split(' ')[0] != hand[1].split(' ')[0]:
            raise Exception('Not suitable for pairs')

        card = hand[0].split(' ')[0]
        if card in ['Ace', '8']:
            return 'Split'
        if card in ['10', 'Jack', 'Queen', 'King']:
            return 'Stand'
        if card == '9':
            return 'Stand' if self.dealers_hand[0].split(' ')[0] in ['7', '10', 'Jack', 'Queen', 'King', 'Ace'] else 'Split'
        if card == '7':
            return 'Hit' if self.dealers_hand[0].split(' ')[0] in ['8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] else 'Split'
        if card == '6':
            return 'Hit' if self.dealers_hand[0].split(' ')[0] in ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] else 'Split'
        if card == '5':
            return 'Hit' if self.dealers_hand[0].split(' ')[0] in ['10', 'Jack', 'Queen', 'King', 'Ace'] else 'Double'
        if card == '4':
            return 'Split' if self.dealers_hand[0].split(' ')[0] in ['5', '6'] else 'Hit'
        if card in ['2', '3']:
            return 'Hit' if self.dealers_hand[0].split(' ')[0] in ['8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] else 'Split'
            
    def ace_in_hand(self, hand: list):
        """
        If there is an ace in the hand, this function will return the recommended action based on the basic strategy.

        Args:
            hand (list): A list of strings representing the cards in the hand (e.g., 'Ace of Clubs', '2 of Hearts').

        Returns:
            str: The recommended action based on the basic strategy. One of 'Hit', 'Stand', 'Double', 'Split'.
        """
        value = self.blackjack_hand_value(hand)
        if type(value) != tuple:
            raise Exception('Not suitable for ace in hand')
        
        value = value[1]
        if value in [19, 20, 21]:
            return 'Stand'
        elif value == 18:
            return 'Stand' if self.dealers_hand[0].split(' ')[0] in ['2', '7', '8'] else 'Double' if self.dealers_hand[0].split(' ')[0] in ['3', '4', '5', '6'] else 'Hit'
        elif value == 17:
            return 'Double' if self.dealers_hand[0].split(' ')[0] in ['3', '4', '5', '6'] else 'Hit'
        elif value in [16, 15]:
            return 'Double' if self.dealers_hand[0].split(' ')[0] in ['4', '5', '6'] else 'Hit'
        elif value in [14, 13]:
            return 'Double' if self.dealers_hand[0].split(' ')[0] in ['5', '6'] else 'Hit'
        elif value == 12: # Only possible if 2 aces
            return 'Split'

    def other_situations(self, hand: list):
        """
        Other situations for blackjack.

        Args:
            hand (list): A list of strings representing the cards in the hand (e.g., 'Ace of Clubs', '2 of Hearts').

        Returns:
            str: The recommended action based on the basic strategy. One of 'Hit', 'Stand', 'Double', 'Split'. 
        """
        value = self.blackjack_hand_value(hand)
        if type(value) != int:
            raise Exception('Not suitable for other situations')
        
        if value >= 17:
            return 'Stand'
        if value in [13, 14, 15, 16]:
            return 'Stand' if self.dealers_hand[0].split(' ')[0] in ['2', '3', '4', '5', '6'] else 'Hit'
        if value == 12:
            return 'Stand' if self.dealers_hand[0].split(' ')[0] in ['4', '5', '6'] else 'Hit'
        if value == 11:
            return 'Double' if self.dealers_hand[0].split(' ')[0] != 'Ace' else 'Hit'
        if value == 10:
            return 'Double' if self.dealers_hand[0].split(' ')[0] not in ['10', 'Jack', 'Queen', 'King', 'Ace'] else 'Hit'
        if value == 9:
            return 'Double' if self.dealers_hand[0].split(' ')[0] in ['3', '4', '5'] else 'Hit'
        if value in [5, 6, 7, 8]:
            return 'Hit'

    def basic_strategy(self, hand: list):
        """
        Basic strategy for blackjack.
        Args:
            hand (list): A list of strings representing the cards in the hand (e.g., 'Ace of Clubs', '2 of Hearts').

        Returns:
            str: The recommended action based on the basic strategy. One of 'Hit', 'Stand', 'Double', 'Split'.
        """
        if len(hand) == 2 and hand[0].split(' ')[0] == hand[1].split(' ')[0]:
            return self.pairs(hand)
        for card in hand:
            if card.split(' ')[0] == 'Ace':
                return self.ace_in_hand(hand)
        return self.other_situations(hand)
    

# Testler
bj = BlackJack()
# IT FUCKING WORKS
# As I tested...
print(bj.basic_strategy(['Ace of Clubs', 'Ace of Hearts', 'Ace of Spades'])) # Split