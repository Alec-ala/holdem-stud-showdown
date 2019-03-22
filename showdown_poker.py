import copy
import distutils.core
from enum import Enum
from time import time
from random import shuffle
from math import floor


#Individual Cards
class Card:
    def __init__ (self,value,suit):
        self.value = value
        self.suit = suit
        self.vname = vname[value]
        self.sname = sname[suit]

    def __str__(self):
        return f'{self.sname}{self.vname}{self.sname}'

    def __repr__(self):
        if self.value <= 10:
            return f'{self.value}{self.suit[0].lower()}'
        if self.value > 10:
            return f'{self.vname[0]}{self.suit[0].lower()}'

#All Decks
class Deck:
    def __init__(self):
        self.cards = []
        self.create()

    def create(self):
        """Generate all of the decks."""
        for _ in range(decks):
            for val in (2,3,4,5,6,7,8,9,10,11,12,13,14):
                for suit in ("Hearts", "Spades", "Clubs", "Diamonds"):
                    self.cards.append(Card(val,suit))
        shuffle(self.cards)

    def draw(self,x):
        """Generate a hand of x cards"""
        for y in range(x):
            drawcards[y] = self.cards.pop()

        return drawcards

class BaseStrength(Enum):
    ROYAL_FLUSH = 10000
    STRAIGHT_FLUSH = 9000
    QUADS = 8000
    FULL_HOUSE = 7000
    FLUSH = 6000
    STRAIGHT = 5000
    SET = 4000
    TWO_PAIR = 3000
    PAIR = 2000
    HIGH_CARD = 1000

#Determine Values and Suits in Hand
def determine(hand):
    """Returns a list of values, a set of values, a list of suits, and a list of cards within a hand."""
    values, vset, suits, all_cards = [], set(), [], []
    for x in range(len(hand)):
        values.append(hand[x].value)
        vset.add(hand[x].value)
        suits.append(hand[x].suit)
        all_cards.append(hand[x])
    return sorted(values,reverse=True),vset,suits,all_cards

#Message/Text Functions
def ss():
    """Prints hand strength if advanced stats are on"""
    if show_strength: print(f'[{round(strength/10000,6)}]')
    else: print()

def hnumber(max_v,msg):
    """Returns the number of hands (int) to be generated given the maximum hands that can be generated"""
    while True:
        try:
            hn = input(msg)
            if hn.lower() == 'm' or hn.lower() == 'max':
                return max_v
            elif 0 < int(hn) <= max_v:
                return int(hn)
            else:
                print(f'Please enter an integer between 1 and {max_v}.')
        except ValueError:
            print('Please enter a positive integer.')

def decks(msg):
    """Returns the number of decks (int) to be generated"""
    while True:
        try:
            d = int(input(msg))
            if d > 0:
                return d
            else:
                print('Please enter a positive integer.')
        except ValueError:
            print('Please enter a positive integer.')

def cph(msg):
    """Returns the number of cards (int) to be included in each hand"""
    while True:
        try:
            d = int(input(msg))
            if 5 <= d <= 52:
                return d
            else:
                print('Please enter a positive integer between 5 and 52.')
        except ValueError:
            print('Please enter a positive integer between 5 and 52.')

def sstrength(msg):
    """Returns a boolean indicating whether advanced stats are shown"""
    while True:
        try:
            ss = distutils.util.strtobool(input(msg))
            if ss == 0 or ss == 1:
                return ss
            else:
                print('Please indicate whether you\'d like to show advanced stats')
        except ValueError:
            print('Please indicate whether you\'d like to show advanced stats')

def get_inputs():
    """Returns a tuple containing the integer outputs of decks(), cph(), hnumber() and the boolean output of sstrength()"""
    decks_ = decks('How many decks are there? ')
    cph_ = cph('How many cards per hand? ')
    max_v = floor((decks_*52)/cph_)
    hnumber_ = hnumber(max_v,f'How many players are there (max {floor((decks_*52)/cph_)})? ')
    sstrength_ = sstrength("Would you like to show advanced stats? ")

    return (decks_,cph_,hnumber_,sstrength_)

def print_hand(user_hand):
    """Pretty prints a single hand"""
    print(f"\nPlayer {h_inc + 1}'s hand:")
    print("| ",end="")
    for c_x in user_hand: print(user_hand[c_x],end=" | ")


def post_draw():
    """Displays various stats if advanced stats are on and displays the strongest and weakest hand if advanced stats is off"""
    hss = sorted(h_strength.items(), key=lambda k: k[1], reverse=True)

    if not show_strength:
        print(f'\n\n\nPlayer {hss[0][0] + 1} has the strongest hand!\nPlayer {hss[hnumber-1][0]+1} has the weakest hand :(')

    if show_strength:

        print(f'\n\n\nPlayer {hss[0][0]+1} has the strongest hand! [{round(hss[0][1]/10000,6)}]\nPlayer {hss[hnumber-1][0] + 1} has the weakest hand :( [{round(hss[hnumber-1][1]/10000,6)}]')

        print('\n\n\n\n\nHand Occurence:\n')
        for x in range(10): print(ho_names[x],hand_occurence[x],f'({round(100*hand_occurence[x]/len(hss),2)}%)')

        print('\n\n\n\n\nFull Player Ranking:\n')
        for x in range(len(hss)): print(f'{x+1}.',f'Player {hss[x][0]+1}',f'[{round(hss[x][1]/10000,6)}]')

        print('\n\n\nComplete Execution Time:', "%ss" % (round(time()-deck_start_time,2)))
        print('Deck Build Time:', '%ss' % (round(deck_end_time-deck_start_time,2)), f'({int(round(100*(deck_end_time-deck_start_time)/(time()-deck_start_time),0))}%)')
        print('Hand Build Time:', '%ss' % (round(time()-deck_end_time,2)), f'({int(round(100*(time()-deck_end_time)/(time()-deck_start_time),0))}%)')


#Evaluation Functions
def hcard(values):
    """Returns the name of a high-card hand (string) given a list of the hand's card values. Also changes hand strength accordingly."""
    global strength
    strength = BaseStrength.HIGH_CARD.value + 10*values[0] + values[1] + .1*values[2] + .01*values[3] + .001*values[4]
    return f'High-Card {vname[values[0]]}'

def numpair(values):
    """Returns the name of a one-pair or two-pair hand (string) given a list of the hand's card values.
    Returns False if one-pair or two-pair is not present within the hand. Also changes hand strength accordingly."""
    global strength
    pairs = list(dict.fromkeys([val for val in values if values.count(val) == 2]))
    if not pairs:
        return False
    if len(pairs) == 1:
        vp = values.copy()
        for _ in range(2):
            vp.remove(pairs[0])
        strength = BaseStrength.PAIR.value + 10*pairs[0] + vp[0] + .1*vp[1] + .01*vp[2];
        return f'Pair of {vname[pairs[0]]}s'
    if len(pairs) >= 2:
        vps = values.copy()
        pairs = sorted(pairs,reverse=True)
        for _ in range(2):
            vps.remove(pairs[0]); vps.remove(pairs[1])
        strength = (BaseStrength.TWO_PAIR.value + 10*int(pairs[0]) + int(pairs[1])) + .1*vps[0]
        return f'{vname[pairs[0]]}s and {vname[pairs[1]]}s'


def trip(values):
    """Returns the name of a three-of-a-kind hand (string) given a list of the hand's card values.
    Returns False if a set is not present within the hand. Also changes hand strength accordingly."""
    global strength
    trips = [val for val in values if values.count(val) == 3]
    if not trips:
        return False
    else:
        vs = values.copy()
        for _ in range(3):
            vs.remove(trips[0])
        strength = BaseStrength.SET.value + 10*trips[0] + vs[0] + .1*vs[1]
        return f'Set of {vname[trips[0]]}s'

def straight(vset,get_vals=False):
    """Returns the name of a straight hand (string) given a set of the hand's card values.
    Returns False if a straight is not present within the hand. Also changes hand strength accordingly.
    If get_vals is true, straight() does not change strength and returns the values present in a straight."""
    global strength
    count = 0

    if not get_vals:
        straight = False
        for rank in (14, *range(2, 15)):
            if rank in vset:
                count += 1
                max_c = rank
                if count == 5:
                    strength = BaseStrength.STRAIGHT.value + 10*min(vset)
                    straight = f'Straight from {vname[max_c-4]} to {vname[max_c]}'
                    break
            else: count = 0
        return straight

    if get_vals:
        sset = set()
        for rank in (14, *range(2, 15)):
            if rank in vset:
                count += 1
                sset.add(rank)
                if count == 5:
                    return sset
            else:
                count = 0
                sset = set()
        raise Exception('No SSET')

def flush(suits,all_cards):
    """Returns the name of a flush hand (string) given a list of the hand's card suits and a list of all the cards in the hand.
    Returns False if a flush is not present within the hand. Also changes hand strength accordingly."""
    global strength
    flushes = [suit for suit in suits if suits.count(suit) >= 5]
    if flushes: flushes_vals = sorted([card.value for card in all_cards if card.suit == flushes[0]],reverse=True)
    if not flushes:
        return False
    else:
        strength = BaseStrength.FLUSH.value + 10*flushes_vals[0] + flushes_vals[1] + .1*flushes_vals[2] + .01*flushes_vals[3] + .001*flushes_vals[4]
        flush = f'{vname[max(flushes_vals)]}-High flush of {flushes[0]}'
    return flush

def fullhouse(values):
    """Returns the name of a filled up (string) hand given a list of the hand's card values.
    Returns False if a full house is not present within the hand. Also changes hand strength accordingly."""
    global strength
    trips = list(dict.fromkeys(sorted([val for val in values if values.count(val) == 3],reverse=True)))
    if not trips:
        return False

    pairs = sorted([val for val in values if values.count(val) == 2],reverse=True)

    if pairs and trips:
        strength = BaseStrength.FULL_HOUSE.value + 10*trips[0] + pairs[0]
        fh = f'{vname[trips[0]]}s full of {vname[pairs[0]]}s'

    if len(trips) > 1:
        if pairs:
            if trips[1] > pairs[0]:
                strength = BaseStrength.FULL_HOUSE.value + 10*trips[0] + trips[1]
                fh = f'{vname[trips[0]]}s full of {vname[trips[1]]}s'
        else:
            strength = BaseStrength.FULL_HOUSE.value + 10*trips[0] + trips[1]
            fh = f'{vname[trips[0]]}s full of {vname[trips[1]]}s'

    if len(trips) == 1 and not pairs:
        return False

    return fh

def quads(values):
    """Returns the name of a four-of-a-kind hand (string) given a list of the hand's card values.
    Returns False if quads are not present within the hand. Also changes hand strength accordingly."""
    global strength
    quads = [val for val in values if values.count(val) >= 4]
    if not quads:
        return False
    else:
        vq = values.copy()
        for _ in range(4): vq.remove(quads[0])
        strength = BaseStrength.QUADS.value + 10*quads[0] + vq[0]
        return f'Quad {vname[quads[0]]}s'

def straightflush(suits,vset,all_cards):
    """Returns the name of a straight or royal flush hand (string) given a list of the hand's card suits,
    a set of the hand's card values, and a list of all the cards in the hand.
    Returns False if a straight or royal flush is not present within the hand. Also changes hand strength accordingly."""
    global strength
    straight_= False

    flushes = [suit for suit in suits if suits.count(suit) >= 5]
    if flushes:
        flushes_vals = sorted([card.value for card in all_cards if card.suit == flushes[0]],reverse=True)

        if straight(flushes_vals):
            straight_vals = straight(flushes_vals,True)
            if {14,10,11,12,13} <= straight_vals: straight_ = "Royal"
            if {14,2,3,4,5} <= straight_vals: straight_ = "Wheel"
            else: straight_ = "Normal"

    if straight_ == "Normal":
        strength = BaseStrength.STRAIGHT_FLUSH.value + 10*max(flushes_vals)
        sf = f'{vname[max(straight_vals)]}-High Straight Flush of {flushes[0]}'
    elif straight_ == "Wheel":
        strength = BaseStrength.STRAIGHT_FLUSH.value
        sf = f'Five-High Straight Flush of {flushes[0]}'
    elif straight_ == "Royal":
        strength = BaseStrength.ROYAL_FLUSH.value
        sf = f'Royal Flush of {flushes[0]}'
    else:
        sf = False
    return sf

def evalhand(values,suits,vset,all_cards):
    """Returns the exact type of hand (string) that is present given a list of values and suits within the hand, a set of values within the hand, and a list of all the cards in the hand"""
    x = straightflush(suits,vset,all_cards)
    if not x: x = quads(values)
    if not x: x = fullhouse(values)
    if not x: x = flush(suits,all_cards)
    if not x: x = straight(values)
    if not x: x = trip(values)
    if not x: x = numpair(values)
    if not x: x = hcard(values)

    return x

def count_hand_occurence(strength):
    """Adjusts hand occurence based on the strength of the current hand"""
    if strength < 2000: hand_occurence[0]+=1
    elif strength < 3000: hand_occurence[1]+=1
    elif strength < 4000: hand_occurence[2]+=1
    elif strength < 5000: hand_occurence[3]+=1
    elif strength < 6000: hand_occurence[4]+=1
    elif strength < 7000: hand_occurence[5]+=1
    elif strength < 8000: hand_occurence[6]+=1
    elif strength < 9000: hand_occurence[7]+=1
    elif strength < 10000: hand_occurence[8]+=1
    elif strength == 10000: hand_occurence[9]+=1

#Main Function
def showdown_poker():
    for h_inc in range(hnumber): #Hand Print Loop
        user_hand = deck.draw(cards_per_hand)
        print_hand(user_hand)

        values,vset,suits,all_cards = determine(user_hand)
        exact_hand = evalhand(values,suits,vset,all_cards)
        print('\n'+exact_hand,end=" "); ss()

        count_hand_occurence(strength)
        h_strength[h_inc] = strength

    post_draw()


hand_occurence = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
ho_names = ['High Card: ','Pair: ','Two-Pair: ','Three of a Kind: ','Straight: ','Flush: ','Full House: ','Four of a Kind: ','Straight Flush: ','Royal Flush: ']

vname = {1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
sname = {"Hearts": '♥', "Spades": '♠', "Clubs": '♣', "Diamonds": '♦'}

drawcards, h_strength = {}, {}

decks, cards_per_hand, hnumber, show_strength = get_inputs()
deck_start_time = time()

deck = Deck()
deck_end_time = time()



if __name__ == '__main__':
    showdown_poker()
