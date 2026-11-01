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


# Chance of winning / pushing / losing if you STAND on a total, against each dealer first card.
# The dealer's hand is simulated once per dealer card and every player total is scored against it.
# Only the dealer's first card is taken out of the shoe (your cards are not known from a total).
data1 = []      # win %
data1p = []     # push %
deal = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
play_sum = list(range(4, 22))
for m in range(500):
    win_row = []
    push_row = []
    wins = {}
    pushes = {}
    for j in deal:
        shoe = make_shoe([j])
        finals = [getsum(j, shoe) for k in range(5000)]
        bust = sum(1 for f in finals if f > 21)
        count = {v: finals.count(v) for v in range(17, 22)}
        for i in play_sum:
            win = bust + sum(count[v] for v in range(17, 22) if v < i)
            push = count[i] if i >= 17 else 0
            wins[(i, j)] = (win / 5000) * 100
            pushes[(i, j)] = (push / 5000) * 100
    for i in play_sum:
        for j in deal:
            win_row.append(wins[(i, j)])
            push_row.append(pushes[(i, j)])
    data1.append(win_row)
    data1p.append(push_row)

df = pd.DataFrame(data1)
df.to_csv(os.path.join(DATA, "DataSet_2_raw.csv"))
dfp = pd.DataFrame(data1p)
dfp.to_csv(os.path.join(DATA, "DataSet_2_push_raw.csv"))

# Average the 500 repetitions into the cleaned tables (rows = your total when standing,
# columns = dealer card). Dataset2_clean.csv is the win %, the others are push % and loss %.
win = pd.DataFrame(df.mean().to_numpy().reshape(len(play_sum), 13), index=play_sum, columns=deal)
push = pd.DataFrame(dfp.mean().to_numpy().reshape(len(play_sum), 13), index=play_sum, columns=deal)
loss = 100 - win - push
for name, table in (("Dataset2_clean.csv", win), ("Dataset2_push_clean.csv", push), ("Dataset2_loss_clean.csv", loss)):
    table.index.name = "sum"
    table.round(3).to_csv(os.path.join(DATA, name))
