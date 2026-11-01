import os
import random
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


data = []
dealer_fc = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
for m in range(500):
    map = {'A':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'10':9,'J':10,'Q':11,'K':12}
    dealer_sum = [0,17,18,19,20,21]
    li = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    for i in dealer_fc:
        shoe = make_shoe([i])
        for j in range(10000):
            deal_sum = getsum(i, shoe)
            map_key = map[i]
            if(deal_sum <= 21):

                li[map_key][deal_sum-16] += 1
            else:
                li[map_key][0] += 1

    p = []
    p_final = []

    for i in li:
        o = []
        for j in i:
            k = j/100
            o.append(k)
        p.append(o)

    for k in p:
        for z in k:
            p_final.append(z)
    data.append(p_final)

df = pd.DataFrame(data)
df.to_csv(os.path.join(DATA, "DataSet_1_raw.csv"))

# Average the 500 repetitions into the cleaned table (rows = dealer card, columns = % of hands
# ending in bust (0) or a final total of 17-21).
clean = pd.DataFrame(df.mean().to_numpy().reshape(13, 6), index=dealer_fc,
                     columns=["0", "17", "18", "19", "20", "21"])
clean.index.name = "card"
clean.round(3).to_csv(os.path.join(DATA, "Dataset1_clean.csv"))
