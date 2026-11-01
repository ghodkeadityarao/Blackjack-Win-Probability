"""Check the simulated tables against an exact calculation of the same rules.

    python check_tables.py

No simulation is used here. For the real shoe (6 decks, cards already on the table taken
out, dealer peeks and stands on every 17) the script works out the exact chance of every
dealer ending, then the exact win / push / loss for every cell of the three tables, and
prints how far the simulated tables are from it (in percentage points).
"""
import os
from functools import lru_cache

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datasets')
DECKS = 6
RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
VAL = {'A': 1, **{str(i): i for i in range(2, 11)}, 'J': 10, 'Q': 10, 'K': 10}
IDX = {r: i for i, r in enumerate(RANKS)}
TENS = ('10', 'J', 'Q', 'K')


def best(total, ace):
    return total + 10 if ace and total + 10 <= 21 else total


def shoe_counts(known):
    counts = [4 * DECKS] * 13
    for r in known:
        counts[IDX[r]] -= 1
    return tuple(counts)


@lru_cache(maxsize=None)
def finish(counts, total, ace):
    """Chance the dealer ends on 17, 18, 19, 20, 21 or busts, from this shoe and hand."""
    out = np.zeros(6)
    if total > 21:
        out[5] = 1
        return out
    b = best(total, ace)
    if b >= 17:
        out[b - 17] = 1
        return out
    n = sum(counts)
    for r in RANKS:
        k = counts[IDX[r]]
        if k:
            c2 = list(counts)
            c2[IDX[r]] -= 1
            out = out + (k / n) * finish(tuple(c2), total + VAL[r], ace or r == 'A')
    return out


def holes(up, counts):
    """The dealer's possible hole cards and their chances, given no dealer blackjack."""
    banned = TENS if up == 'A' else ('A',) if up in TENS else ()
    allowed = [r for r in RANKS if r not in banned and counts[IDX[r]]]
    n = sum(counts[IDX[r]] for r in allowed)
    return [(r, counts[IDX[r]] / n) for r in allowed]


def dealer_dist(up, counts):
    out = np.zeros(6)
    for h, p in holes(up, counts):
        c2 = list(counts)
        c2[IDX[h]] -= 1
        out += p * finish(tuple(c2), VAL[up] + VAL[h], 'A' in (up, h))
    return out


def win_push_loss(d, total):
    """Percent win / push / loss when standing on `total` against dealer distribution d."""
    win = d[5] + (d[:total - 17].sum() if total >= 17 else 0.0)
    push = d[total - 17] if total >= 17 else 0.0
    return 100 * win, 100 * push, 100 * (1 - win - push)


def read(name, index):
    return pd.read_csv(os.path.join(DATA, name)).set_index(index)


def check_dealer():
    t = read('Dataset1_clean.csv', 'card')
    t.index = t.index.astype(str)
    errors = []
    for c in RANKS:
        d = dealer_dist(c, shoe_counts([c]))
        exact = 100 * np.array([d[5], *d[:5]])
        errors.append(t.loc[c, ['0', '17', '18', '19', '20', '21']].to_numpy(float) - exact)
    return np.array(errors)


def check_stand():
    win, push, loss = (read(f'Dataset2_{x}clean.csv', 'sum') for x in ('', 'push_', 'loss_'))
    errors = []
    for c in RANKS:
        d = dealer_dist(c, shoe_counts([c]))
        for total in win.index:
            ew, ep, el = win_push_loss(d, int(total))
            errors += [win.loc[total, c] - ew, push.loc[total, c] - ep, loss.loc[total, c] - el]
    return np.array(errors)


def check_hit_once():
    win, push, loss = (read(f'Dataset3_{x}clean.csv', 'sum1') for x in ('', 'push_', 'loss_'))
    errors = []
    for a in RANKS:
        for b in RANKS:
            for k in RANKS:
                counts = shoe_counts([a, b, k])
                w = p = 0.0
                for hole, p_hole in holes(k, counts):
                    c1 = list(counts)
                    c1[IDX[hole]] -= 1
                    n = sum(c1)
                    for r in RANKS:
                        m = c1[IDX[r]]
                        if not m:
                            continue
                        total = best(VAL[a] + VAL[b] + VAL[r], 'A' in (a, b, r))
                        if total > 21:
                            continue  # busted: a loss
                        c2 = list(c1)
                        c2[IDX[r]] -= 1
                        d = finish(tuple(c2), VAL[k] + VAL[hole], 'A' in (k, hole))
                        ew, ep, _ = win_push_loss(d, total)
                        w += p_hole * (m / n) * ew
                        p += p_hole * (m / n) * ep
                row = a + b
                errors += [win.loc[row, k] - w, push.loc[row, k] - p, loss.loc[row, k] - (100 - w - p)]
    return np.array(errors)


if __name__ == '__main__':
    print(f"{'Table':<40}{'Numbers':>9}{'Avg error':>11}{'Worst error':>13}")
    for name, fn in (("Dealer's final hand (Dataset 1)", check_dealer),
                     ('Stand: win, push, loss (Dataset 2)', check_stand),
                     ('Hit once: win, push, loss (Dataset 3)', check_hit_once)):
        e = np.abs(fn())
        print(f'{name:<40}{e.size:>9,}{e.mean():>10.2f} {e.max():>12.2f}   (percentage points)')
