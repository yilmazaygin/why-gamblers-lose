import random

class BlackJack:
    def __init__(self): 
        self.dealers_hand = ['4 of Clubs', '10 of Hearts']
        self.shoe = self.create_shoe(1)
        self.shoe = self.shuffle_shoe(self.shoe)

    def create_shoe(self, num_decks):
        """Kart destesini oluşturur.""" 
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        shoe = [f'{rank} of {suit}' for suit in suits for rank in ranks] * num_decks
        return shoe

    def shuffle_shoe(self, shoe):
        """Kartları karıştırır.""" 
        random.shuffle(shoe)
        return shoe

    def deal(self, shoe):
        """Bir kart çeker.""" 
        return shoe.pop()

    def blackjack_hand_value(self, hand):
        """Bir elin değerini hesaplar."""
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

        return total_value

    def dealer_play(self):
        """Krupiyenin oynama mantığı.""" 
        while self.blackjack_hand_value(self.dealers_hand) < 17:
            self.dealers_hand.append(self.deal(self.shoe))
        return self.dealers_hand

class BJPlayer:
    def __init__(self, bal, first_bet):
        self.balance = bal
        self.bets = [first_bet]
        self.hands = [[]]

    def add_hand(self, hand):
        """Yeni bir el ekler.""" 
        self.hands.append(hand)
        self.bets.append(self.bets[0])

    def reset_hands(self):
        """Eller sıfırlanır.""" 
        self.hands = [[]]
        self.bets = [self.bets[0]]

    def update_balance(self, amount):
        """Bakiye günceller.""" 
        self.balance += amount

    def martingale(self):
        """Martingale stratejisini kontrol eder.""" 
        if self.balance <= 0:
            print("Player has no balance left.")
            return False
        if self.balance < self.bets[0]:
            print("Player cannot place the bet.")
            return False
        return True

    def can_double(self):
        """Oyuncunun double yapıp yapamayacağını kontrol eder."""
        if self.balance < self.bets[0]:
            print("Player cannot double due to insufficient balance.")
            return False
        return True

    def can_split(self):
        """Oyuncunun split yapıp yapamayacağını kontrol eder."""
        if self.balance < self.bets[0]:
            print("Player cannot split due to insufficient balance.")
            return False
        return True

    def play_round(self, game):
        """Bir elde yapılacak hamleyi belirler.""" 
        for hand in self.hands:
            value = game.blackjack_hand_value(hand)
            if value > 21:
                print(f"Player busts with hand: {hand}")
                self.update_balance(-self.bets[0])
            elif value == 21 and len(hand) == 2:
                print(f"Player gets Blackjack with hand: {hand}")
                self.update_balance(1.5 * self.bets[0])
            else:
                # Oyuncunun stratejisine göre hamle yapılacak
                if value == 9 and self.can_double():
                    print(f"Player doubles with hand: {hand}")
                    self.update_balance(-self.bets[0])
                    hand.append(game.deal(game.shoe))
                elif value == 10 and self.can_double():
                    print(f"Player doubles with hand: {hand}")
                    self.update_balance(-self.bets[0])
                    hand.append(game.deal(game.shoe))
                elif value == 11 and self.can_double():
                    print(f"Player doubles with hand: {hand}")
                    self.update_balance(-self.bets[0])
                    hand.append(game.deal(game.shoe))
                elif len(hand) == 2 and hand[0].split(' ')[0] == hand[1].split(' ')[0] and self.can_split():
                    print(f"Player splits with hand: {hand}")
                    self.add_hand([hand[1], game.deal(game.shoe)])
                    hand[1] = game.deal(game.shoe)
                else:
                    print(f"Player stands with hand: {hand}")

# Oyun başlatma
def main():
    # Oyunun başlatılması
    player_balance = 1000  # Oyuncunun başlangıç bakiyesi
    initial_bet = 50  # İlk bahis miktarı

    game = BlackJack()  # BlackJack oyunu başlatılıyor
    player = BJPlayer(player_balance, initial_bet)  # Oyuncu başlatılıyor

    # Oyunun simülasyonu başlatılıyor
    print("Game start!")
    print(f"Player balance: {player.balance}")
    print(f"Initial bet: {player.bets[0]}")

    while player.balance > 0 and player.balance < 2000:
        # Bir tur başlatılıyor
        print(f"\nStarting new round, Player balance: {player.balance}")

        # Oyuncuya kart dağıtılır
        player.hands[0] = [game.deal(game.shoe), game.deal(game.shoe)]
        print(f"Player's hand: {player.hands[0]}")

        # Oyuncunun stratejisini uygula
        player.play_round(game)

        # Krupiyenin oyunu
        print(f"Dealer's hand: {game.dealers_hand}")
        game.dealer_play()
        print(f"Dealer's final hand: {game.dealers_hand}")

        # Sonuçlar
        player_balance = player.balance
        print(f"Player's balance after round: {player_balance}")

        # Eğer oyuncu kaybederse Martingale stratejisi uygulanacak
        if player.balance <= 0:
            print("Player has lost all balance. Game Over.")
            break
        elif player.balance >= 2000:
            print("Player has doubled their balance. Game Over.")
            break

        # Bahis iki katına çıkar
        player.bets[0] *= 2
        print(f"Next bet: {player.bets[0]}")

if __name__ == "__main__":
    main()
