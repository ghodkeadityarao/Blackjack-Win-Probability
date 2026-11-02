# Blackjack Win Probability

**Live app:** [https://blackjackwinprobability.streamlit.app](https://blackjackwinprobability.streamlit.app/)

Simulated blackjack odds: the chance of winning, pushing and losing a hand against every dealer card, from a 6-deck shoe with the dealer peeking for blackjack. Every number is checked against an exact calculation (worst error 0.74 percentage points), and a Streamlit web app (`app.py`) looks up any starting hand.

For example, with an 18 (an 8 and a 10) against a dealer 6:

| Play | Win | Push | Lose |
|---|---|---|---|
| Stand on 18 | 58.9% | 10.6% | 30.5% |
| Hit once, then stand | 18.6% | 2.5% | 78.9% |

Blackjack, also known as 21, is a popular card game often played in casinos. The goal of the game is to beat the dealer by having a hand value that is closer to 21 than the dealer's hand value, without exceeding 21. Here are the basic rules of the game:

# Card Values:

Number cards (2-10): Their face value (e.g., a 5 is worth 5 points).
Face cards (Jack, Queen, King): Each worth 10 points.
Ace: Can be worth either 1 point or 11 points, depending on which value benefits the player more. It's flexible and can change during the course of a hand.

# Gameplay:

Blackjack's goal is to get a hand close to 21 without exceeding it, beating the dealer. Players and the dealer are dealt two cards. Players' cards are face-up; the dealer has one upcard and one face-down (hole card).

Players choose actions based on hand value:

"Hit" for another card, aiming to get closer to 21.
"Stand" to keep current total.
"Surrender" forfeits half the bet if the hand seems weak.
After players act, the dealer reveals their hole card. The dealer must hit until 17 (or more) is reached. Some hit on "soft 17" (Ace-6), while others stand.

If the dealer busts (exceeds 21), players win. If not, hands are compared. Players with higher hands win.

These rules offer a concise overview of blackjack. Strategy involves judging card values, dealer's upcard, and making decisions to maximize winning chances while avoiding busting.
# Winning:

Players win even money on their bets if they have a higher hand total than the dealer without exceeding 21.
If a player's hand value is exactly 21, they have a "blackjack".
If the player's hand total exceeds 21, they bust and lose their bet.
It's important to note that blackjack rules can vary slightly between different casinos and regions. Before playing, it's a good idea to familiarize yourself with the specific rules of the game you're participating in.

# Our Objective:

Calculating the exact probabilities in blackjack can be quite complex due to the changing nature of the deck as cards are drawn.

In the first case, when the dealer's card is shown, calculating the probability(in %) of winning in blackjack involves considering the player's hand value and the dealer's visible card. By analyzing these factors, the player can estimate their chances of winning based on potential outcomes.

**Dealer's final hand, % of hands (by dealer's first card)**

| Dealer card   |   Bust |   17 |   18 |   19 |   20 |   21 |
|:--------------|-------:|-----:|-----:|-----:|-----:|-----:|
| A             |   16.7 | 18.8 | 18.9 | 18.9 | 18.9 |  7.7 |
| 2             |   35.4 | 14   | 13.5 | 13   | 12.4 | 11.8 |
| 3             |   37.4 | 13.4 | 13.1 | 12.5 | 12.1 | 11.5 |
| 4             |   39.6 | 13.1 | 12.4 | 12.1 | 11.6 | 11.2 |
| 5             |   41.8 | 12.2 | 12.2 | 11.7 | 11.2 | 10.8 |
| 6             |   42.3 | 16.6 | 10.6 | 10.7 | 10.2 |  9.7 |
| 7             |   26.2 | 36.9 | 13.8 |  7.9 |  7.9 |  7.4 |
| 8             |   24.4 | 12.9 | 36   | 12.9 |  6.9 |  7   |
| 9             |   22.9 | 12.1 | 11.7 | 35.2 | 12   |  6.1 |
| 10            |   23   | 12.1 | 12.1 | 12.2 | 36.8 |  3.8 |
| J             |   23   | 12.1 | 12.1 | 12.1 | 36.8 |  3.8 |
| Q             |   23   | 12.1 | 12.1 | 12.1 | 36.9 |  3.8 |
| K             |   23   | 12.1 | 12.1 | 12.1 | 36.8 |  3.8 |

In the second case, when the dealer's card is shown and the player has two initial cards, the probabilities change based on whether the player chooses to "hit" (take an additional card) or "stand" (keep the current hand). 

If the player chooses "hit," the probability of winning depends on the likelihood of drawing a card that improves the hand without exceeding 21. 

If the player opts to "stand," the probability of winning is determined by the dealer's eventual hand and whether it surpasses 21 or not.

**Win %, if you stand on a total (rows) against the dealer's first card (columns).** Push and loss are in `Dataset2_push_clean.csv` and `Dataset2_loss_clean.csv`. Totals of 17 or less all give the same chance, because the dealer always ends on 17 or more, so you only win if the dealer busts.

| Your total   |    A |    2 |    3 |    4 |    5 |    6 |    7 |    8 |    9 |   10 |    J |    Q |    K |
|:-------------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| 17 or less   | 16.7 | 35.3 | 37.4 | 39.6 | 41.9 | 42.3 | 26.2 | 24.4 | 22.9 | 23   | 23   | 23   | 23   |
| 18           | 35.5 | 49.3 | 50.9 | 52.6 | 54.1 | 58.9 | 63.1 | 37.2 | 35   | 35.2 | 35.2 | 35.1 | 35.1 |
| 19           | 54.4 | 62.7 | 63.9 | 65   | 66.3 | 69.5 | 76.9 | 73.3 | 46.7 | 47.2 | 47.3 | 47.2 | 47.2 |
| 20           | 73.3 | 75.7 | 76.4 | 77.1 | 78.1 | 80.1 | 84.8 | 86.1 | 81.9 | 59.4 | 59.4 | 59.4 | 59.4 |
| 21           | 92.3 | 88.1 | 88.5 | 88.8 | 89.2 | 90.3 | 92.6 | 93.1 | 93.9 | 96.2 | 96.2 | 96.2 | 96.2 |

# Rules and Accuracy Check

These tables are made by Monte Carlo simulation under these rules:

- **A real shoe.** Cards are dealt from a 6-deck shoe without replacement, so the cards already on the table are taken out first. The dealer's first card is always removed. The "hit once" table also removes your two cards. The "stand" table does not, because a total does not tell us which cards made it.
- **The dealer peeks.** With an ace or a ten-value card showing, the dealer checks for blackjack first. Hands where the dealer has blackjack are left out, so every probability is for a hand that is still being played. That is why a dealer ace shows only 7.7% for a final 21. How often the dealer actually has blackjack is not in the tables: about 31% with an ace showing and 7.7% with a ten.
- **The dealer's play.** The dealer stands on every 17, including soft 17. An ace counts as 11 whenever that does not bust the hand.
- **Win, push and loss are separate.** A tie is a push, not a win. The `*_clean.csv` files hold the win %, the `*_push_clean.csv` files the push %, and the `*_loss_clean.csv` files the loss %. The three add up to 100.
- **"Hit" means one card, then stand.** The hit table (Dataset 3) is "hit once, then stand". It is not the odds of the best play after hitting. Going over 21 is a loss.
- **Not covered:** your own blackjack (A plus a ten-value card, which pays 3:2), doubling, splitting and surrender.

Every number was then checked against an exact calculation of the same rules (a recursion over every possible dealer hand with the real shoe composition), with no simulation involved (`Blackjack win/main/check_tables.py` reproduces this table):

| Table | Numbers checked | Average error | Worst error |
|---|---|---|---|
| Dealer's final hand (Dataset 1) | 78 | 0.01 points | 0.04 points |
| Stand: win, push, loss (Dataset 2) | 702 | 0.01 points | 0.06 points |
| Hit once: win, push, loss (Dataset 3) | 6,591 | 0.13 points | 0.74 points |

What is left is simulation noise. The hit table averages 10 runs while the others average 500, which is why its error is the largest.

# What's in the Repo

- **`app.py`**: a Streamlit web app. Pick the dealer's first card and your two cards and it shows the win, push and lose chances if you stand or hit once, and how the dealer's hand ends.
- **`Blackjack win/main/dataset1_creation.py`, `dataset2_creation.py`, `dataset3_creation.py`**: the simulations that build the three tables (dealer's final hand, stand, hit once).
- **`Blackjack win/main/check_tables.py`**: the exact calculation every table is checked against.
- **`Blackjack win/datasets/`**: the raw simulation output and the cleaned tables, with separate win, push and loss files.
