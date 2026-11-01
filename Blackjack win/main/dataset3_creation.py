import os
import random
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datasets')

DECKS = 6   # cards are dealt from a 6-deck shoe, without replacement
RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
TENS = ('10','J','Q','K')
card_dic = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}


def make_shoe(known):
    # A full shoe with the cards already on the table (known) taken out.
    shoe = [r for r in RANKS for _ in range(4 * DECKS)]
    for r in known:
        shoe.remove(r)
    return shoe


def draw(shoe, used, banned=()):
    # Deal one card without replacement. `used` holds the positions already dealt this hand.
    while True:
        i = random.randrange(len(shoe))
        if i not in used and shoe[i] not in banned:
            used.append(i)
            return shoe[i]


def deal_hole(up, shoe, used):
    # The dealer peeks for blackjack, so hands where the dealer has it are left out:
    # every probability here is for a hand that is still being played.
    banned = TENS if up == 'A' else ('A',) if up in TENS else ()
    return draw(shoe, used, banned)


def dealer_finish(total, ace, shoe, used):
    # Dealer stands on any 17 or more (including soft 17). An ace counts as 11
    # whenever that does not bust the hand. Returns the final total (>21 = bust).
    while True:
        best = total + 10 if ace and total + 10 <= 21 else total
        if best >= 17:
            return best
        card_pick = draw(shoe, used)
        total += card_dic[card_pick]
        ace = ace or card_pick == 'A'


def getsum(up, shoe):
    # Final dealer total for one hand, given the dealer's first card.
    used = []
    hole = deal_hole(up, shoe, used)
    return dealer_finish(card_dic[up] + card_dic[hole], 'A' in (up, hole), shoe, used)


# Chance of winning / pushing / losing if you HIT ONCE and then stand, for every pair of starting
# cards (rows) against every dealer first card (columns). Your two cards, the dealer's first card
# and every card drawn after that are dealt from one shoe. Going over 21 is a loss.
def hit_total(card1, card2, card_pick):
    total = card_dic[card1] + card_dic[card2] + card_dic[card_pick]
    ace = 'A' in (card1, card2, card_pick)
    return total + 10 if ace and total + 10 <= 21 else total


data2 = []     # win %
data2p = []    # push %
deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
for m in range(10):
    map = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}
    arr = np.zeros((169, 13))
    arr_push = np.zeros((169, 13))
    for i in deck:
        for j in deck:
            for k in deck:
                shoe = make_shoe([i, j, k])
                c = 0
                p = 0
                for l in range(5000):
                    used = []
                    hole = deal_hole(k, shoe, used)
                    play_deal = hit_total(i, j, draw(shoe, used))
                    if play_deal > 21:
                        continue
                    card_deal = dealer_finish(card_dic[k] + card_dic[hole], 'A' in (k, hole), shoe, used)
                    if card_deal > 21 or play_deal > card_deal:
                        c += 1
                    elif play_deal == card_deal:
                        p += 1
                req = (((map[i]+1)*13) - (12 - map[j])-1)
                arr[req][map[k]] += c/50
                arr_push[req][map[k]] += p/50
    data2.append(arr.flatten().tolist())
    data2p.append(arr_push.flatten().tolist())

df2 = pd.DataFrame(data2)
df2.to_csv(os.path.join(DATA, "DataSet_3_raw.csv"))
df2p = pd.DataFrame(data2p)
df2p.to_csv(os.path.join(DATA, "DataSet_3_push_raw.csv"))

# Average the 10 repetitions into the cleaned tables (rows = your two cards, columns = dealer card).
# Dataset3_clean.csv is the win %, the others are push % and loss %.
rows = [i + j for i in deck for j in deck]
win = pd.DataFrame(df2.mean().to_numpy().reshape(169, 13), index=rows, columns=deck)
push = pd.DataFrame(df2p.mean().to_numpy().reshape(169, 13), index=rows, columns=deck)
loss = 100 - win - push
for name, table in (("Dataset3_clean.csv", win), ("Dataset3_push_clean.csv", push), ("Dataset3_loss_clean.csv", loss)):
    table.index.name = "sum1"
    table.round(3).to_csv(os.path.join(DATA, name))
