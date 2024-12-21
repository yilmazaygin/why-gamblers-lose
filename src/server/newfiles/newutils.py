import random

def create_shoe(deck_amount: int):
    """
    Creates a shoe with the given number of decks.

    Args:
        deck_amount (int): Number of decks in the shoe.
    """
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    shoe = [rank + " of " + suit for suit in suits for rank in ranks]
    shoe = shoe * deck_amount
    return shoe

def shuffle_shoe(shoe: list):
    """
    Shuffles the created shoe.

    Args:
        shoe (list): List of cards in the shoe.
    
    Returns:
        list: Shuffled shoe.
    """
    random.shuffle(shoe)
    return shoe


def deal(shoe: list, card_receivers: list, times: int): # Deals the cards to the card_receivers, times times
    """
    Deals the cards to the card receivers one by one.
    Note that dealer is a receiver too.

    Args:
        deck (list): List of cards in the deck.
        card_receivers (list): List of lists of card receivers.
        times (int): Number of times the cards will be dealt.
    """  
    for _ in range(times):
        for receiver in card_receivers:
            receiver.append(shoe.pop())

def reset_hands(hands: list, hand_values: list):
    """
    Resets every hand in the game

    Args:
        hands (list): List of hands.
    """
    for hand in hands:
        hand.clear()
    
    for hand_value in hand_values:
        hand_value = 0