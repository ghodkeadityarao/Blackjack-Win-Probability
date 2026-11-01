"""Blackjack win probability: look up the chance of winning, pushing and losing a hand.

    streamlit run app.py

Reads the simulated tables in "Blackjack win/datasets". Rules: 6-deck shoe, dealer peeks for
blackjack and stands on every 17. See the README for what the tables do and do not cover.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "Blackjack win" / "datasets"
CARDS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUE = {"A": 1, **{str(i): i for i in range(2, 11)}, "J": 10, "Q": 10, "K": 10}
TENS = ("10", "J", "Q", "K")
DECKS = 6

st.set_page_config(page_title="Blackjack win probability", layout="centered")


@st.cache_data
def load(name, index):
    return pd.read_csv(DATA / name).set_index(index)


def best_total(c1, c2):
    total = VALUE[c1] + VALUE[c2]
    soft = "A" in (c1, c2) and total + 10 <= 21
    return (total + 10 if soft else total), soft


def show_outcome(title, win, push, loss):
    st.subheader(title)
    a, b, c = st.columns(3)
    a.metric("Win", f"{win:.1f}%")
    b.metric("Push", f"{push:.1f}%")
    c.metric("Lose", f"{loss:.1f}%")


st.title("Blackjack win probability")
st.caption("6 decks, dealer peeks for blackjack and stands on every 17.")

col1, col2, col3 = st.columns(3)
dealer = col1.selectbox("Dealer's first card", CARDS, index=5)
card1 = col2.selectbox("Your first card", CARDS, index=7)
card2 = col3.selectbox("Your second card", CARDS, index=9)

total, soft = best_total(card1, card2)
is_blackjack = "A" in (card1, card2) and (card1 in TENS or card2 in TENS)

if is_blackjack:
    st.success("Blackjack! It pays 3:2 unless the dealer also has blackjack, in which case it is a push.")
    st.caption("Blackjack payouts are not part of the simulated tables.")
else:
    label = f"{'soft ' if soft else ''}{total}"
    stand = [load(f, "sum").loc[total, dealer] for f in
             ("Dataset2_clean.csv", "Dataset2_push_clean.csv", "Dataset2_loss_clean.csv")]
    show_outcome(f"If you stand on {label}", *stand)

    hit = [load(f, "sum1").loc[card1 + card2, dealer] for f in
           ("Dataset3_clean.csv", "Dataset3_push_clean.csv", "Dataset3_loss_clean.csv")]
    show_outcome("If you hit once, then stand", *hit)
    st.caption("This is not the best play after hitting. It only covers drawing one card and then "
               "standing. Going over 21 is a loss.")

d1 = load("Dataset1_clean.csv", "card")
d1.index = d1.index.astype(str)
row = d1.loc[dealer]
st.subheader(f"How the dealer's hand ends (showing {dealer})")
chart = pd.Series(row.to_numpy(float), index=["Bust", "17", "18", "19", "20", "21"], name="% of hands")
st.bar_chart(chart)

if dealer == "A" or dealer in TENS:
    tens_left = 4 * DECKS * 4
    aces_left = 4 * DECKS
    cards_left = 52 * DECKS - 1
    p_bj = (tens_left if dealer == "A" else aces_left) / cards_left
    st.caption(f"All of these are for a hand that is still being played. With a {dealer} showing, the dealer "
               f"has blackjack about {p_bj:.1%} of the time, and those hands are not in the numbers above.")

with st.expander("What these numbers cover"):
    st.markdown(
        """
- Cards come from a 6-deck shoe without replacement, with the cards already on the table removed.
  The "stand" numbers only remove the dealer's first card, since a total does not say which cards made it.
- The dealer peeks for blackjack, so hands where the dealer has it are left out.
- The dealer stands on every 17, including soft 17.
- A tie is a **push**, not a win. Win, push and lose add up to 100%.
- "Hit once" means draw exactly one card, then stand.
- Not covered: your own blackjack payout, doubling, splitting and surrender.
- Simulated numbers were checked against an exact calculation (`Blackjack win/main/check_tables.py`):
  worst error 0.74 percentage points.
"""
    )
