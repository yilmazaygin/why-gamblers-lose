import random

class Baccarat: 
    def __init__(self) -> None:
        pass

    def deck_creator(self, deck_amount):
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        deck = [rank + " of " + suit for suit in suits for rank in ranks]
        deck = deck * deck_amount
        return deck

    def shuffle_deck(self, deck):
        random.shuffle(deck)
        return deck

    def value_of_hand(self, hand):
        value = 0
        values = {"Ace":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":0, "Jack":0, "Queen":0, "King":0}
        for card in hand:
            card_value = card.split(" ")[0]
            value += values[card_value]
        return value % 10

    def player_play(self, hand_value):
        if hand_value in [0, 1, 2, 3, 4, 5]:
            return True
        elif hand_value in [6, 7, 8, 9]:
            return False

    def banker_play(self, hand_value, player_third_card=None):
        if hand_value in [0, 1, 2]:
            return True
        elif hand_value == 3:
            return player_third_card != 8 
        elif hand_value == 4:
            return player_third_card in [2, 3, 4, 5, 6, 7]
        elif hand_value == 5:
            return player_third_card in [4, 5, 6, 7]
        elif hand_value == 6:
            return player_third_card in [6, 7]
        elif hand_value == 7:
            return False
        else:
            return False

    def deal_hand(self, deck):
        return [deck.pop(), deck.pop()]

    def play_game(self):
        deck = self.deck_creator(8)
        deck = self.shuffle_deck(deck)

        player_hand = self.deal_hand(deck)
        banker_hand = self.deal_hand(deck)

        player_value = self.value_of_hand(player_hand)
        banker_value = self.value_of_hand(banker_hand)

        if self.player_play(player_value):
            player_hand.append(deck.pop())
            player_value = self.value_of_hand(player_hand)

        if self.banker_play(banker_value, player_hand[-1] if len(player_hand) > 2 else None):
            banker_hand.append(deck.pop())
            banker_value = self.value_of_hand(banker_hand)

        print(f"Player Hand: {player_hand} -> {player_value}")
        print(f"Banker Hand: {banker_hand} -> {banker_value}")


        # Edit player balances here
        if player_value > banker_value:
            return "Player Wins!"
        elif banker_value > player_value:
            return "Banker Wins!"
        else:
            return "Tie!"

game = Baccarat()
print(game.play_game())
