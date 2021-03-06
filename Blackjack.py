import random
from time import sleep

suits = ('♦', '♣', '♥', '♠')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

# Card object
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (f'{self.rank}{self.suit}')

# Deck object
class Deck:
    def __init__(self):
        # Adds cards into deck with suits and number on them.
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        s = ''
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + '\n'
        return s

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        is_empty = False
        if len(self.deck) == 0:
            is_empty = True
        if is_empty == False:
            return self.deck.pop()
        else:
            print('The deck is empty!')

# Hand object
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    # Ace will either be a 1 or 11.
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Chip object
class Chips:
    def __init__(self, total=0, bet=0):
        self.total = total
        self.bet = bet

    def win_bet(self):
        self.total = self.total + self.bet

    def lose_bet(self):
        self.total = self.total - self.bet

# Asks player how much they would like to bet.
def take_bet():
    taken = False
    while not taken:
        try:
            bet = int(input("How much would you like to bet? You cannot bet more than you have."))
        except BaseException:
            print('Please give me an integer amount: ')
            continue
        if isinstance(bet, int):
            taken = True
    return bet

# Asks player how many chips they would like to begin with.
def take_total():
    taken = False
    while not taken:
        try:
            total = int(input("How many chips would you like to play with? "))
        except BaseException:
            print('Please give me an integer amount: ')
            continue
        if isinstance(total, int):
            taken = True
    return total

# Receives a card from the deck.
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Asks player if they want to hit or stand.
def hit_or_stand(deck, hand):
    global playing
    hit_stand = False
    while hit_stand == False:
        print('\n' * 2)
        question = input('Would you like to Hit or Stand? ')
        if question.lower() == 'hit':
        	print('You draw...\n')
        	sleep(2)
        	hit(deck, hand)
        	print(f'You drew a [{player.cards[-1]}]\n')
        	hit_stand = True
        elif question.lower() == 'stand':
            playing = False
            hit_stand = True

# One of the dealer's card is to remain facedown.
def show_some(player, dealer):
    print("The Dealer's cards are:") 
    print('\n')
    print('[Hidden]')
    for i in range(1, len(dealer.cards)):
        print('[' + str(dealer.cards[i]) + ']')
    print('\n')
    print('-------------------------')
    print('Your cards are: ')
    print('\n')
    for n in range(len(player.cards)):
        print('[' + str(player.cards[n]) + ']')
    print('\n')
    print(f'Your value is: {player.value}')

# Shows every card dealt.
def show_all(player, dealer):
    print("The Dealer's cards are: ")
    print('\n')
    for i in range(len(dealer.cards)):
        print('[' + str(dealer.cards[i]) + ']')
    print('\n')
    print(f'Dealer value is: {dealer.value}')
    print('-------------------------')
    print('Your cards are: ')
    print('\n')
    for n in range(len(player.cards)):
        print('[' + str(player.cards[n]) + ']')
    print('\n')
    print(f'Your value is: {player.value}')

# Player's hand exceeds 21
def player_busts():
    player.value = 0
    print('You bust! Your value is now 0.')

# Player wins
def player_wins():
    if dealer.value < player.value and player.value < 22:
        print('Player wins!')
        return player_chips.win_bet()

# Dealer's hand exceeds 21
def dealer_busts():
    dealer.value = 0
    print('Dealer Busts!')

# Dealer wins
def dealer_wins():
    if player.value < dealer.value and dealer.value < 22:
        print('Dealer wins!')
        return player_chips.lose_bet()

# The game is tied.
def push():
    if dealer.value == player.value:
        print('It is a push!')

# Asks if the player would like to replay or not.
def replay():
    yes_no = False
    while not yes_no:
        replay = input(f'Your amount is {player_chips.total}. Would you like to play again? Please say Yes or No. ')
        if replay.lower() == 'yes':
            if player_chips.total == 0:
                print('Sorry, the amount of chips you own is 0. You can no longer play.')
                break
            yes_no = True
        elif replay.lower() == 'no':
            break

    return yes_no

# Controls the logic of the game.
def play():
    print('Welcome to BlackJack!\n')
    total = take_total()
    # Controls the game loop
    playing = True
    while True:
        # Initial game set-up, player drawing cards.
        deck = Deck()
        deck.shuffle()
        player = Hand()
        dealer = Hand()
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

        # Take player's bet
        bet = take_bet()
        while bet > total:
            bet = take_bet()
        player_chips = Chips(total, bet)
        print('\n')
        
        
        # Plays until player decide to stand or bust
        while playing:
            show_some(player, dealer)
            hit_or_stand(deck, player)
            
            if player.value > 21:
                player_busts()
                break
        print('\n')
        show_all(player, dealer)
        print('\n')
        if player.value == 0:
            dealer_wins()

        # If dealer's hand is below 18, dealer's turn begins
        while dealer.value < 18 and player.value != 0:
            hit(deck, dealer)
            print('\nDealer draws...')
            sleep(2)
            print(f'Dealer drew a [{dealer.cards[-1]}]\n')
            show_all(player, dealer)
            

            if dealer.value > 21:
                dealer_busts()
                player_wins()
                break
        # If both party hasn't bust, the hand with the higher value wins
        if dealer.value >= 17 and player.value != 0:
            if player_wins():
                break
            elif dealer_wins():
                break
            if push():
                break

        # Shows both hands
        print("\n")

        # Asks if player wants to go again.
        if not replay():
            print(
                f'Thank for playing!! You started with {total} this round and now have {player_chips.total}. ')
            if player_chips.total < 0:
                print(f'You owe us {abs(player_chips.total)}.')
            break
        else:
            total = player_chips.total
            playing = True

# Executes the game.
if __name__ == '__main__':
    play()