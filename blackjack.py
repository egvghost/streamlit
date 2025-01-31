'''
    Rules:
      Try to get as close to 21 without going over.
      Kings, Queens, and Jacks are worth 10 points.
      Aces are worth 1 or 11 points.
      Cards 2 through 10 are worth their face value.
      (H)it to take another card.
      (S)tand to stop taking cards.
      On your first play, you can (D)ouble down to increase your bet
      but must hit exactly one more time before standing.
      In case of a tie, the bet is returned to the player.
      The dealer stops hitting at 17.
'''

import random
import time
import streamlit as st

# Constants:
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
numbers = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
suits = [HEARTS, DIAMONDS, SPADES, CLUBS]

# Initialize Streamlit app
st.title("Blackjack")

blackjack_logo = '''
.--------.            _     _            _    _            _    
| A_  _  |           | |   | |          | |  (_)          | |   
| ( \/ ).--------.   | |__ | | __ _  ___| | ___  __ _  ___| | __
|  \\  / | K /\\   |   | '_ \\| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|   \\/ A|  /  \\  |   | |_) | | (_| | (__|   <| | (_| | (__|   < 
'-------|  \\  /  |   |_.__/|_|\\__,_|\\___|_|\\_\\ |\\__,_|\\___|_|\\_\\ 
        |   \\/ K |                          _/ |                
        '--------'                         |__/                 
'''

# Display the logo
st.code(blackjack_logo, language='text')

def hit():
    new_card = {suits[random.randint(0, 3)]: numbers[random.randint(0, 12)]}
    for k, v in new_card.items():
        while v in st.session_state.given_cards[k]:
            new_card = {suits[random.randint(0, 3)]: numbers[random.randint(0, 12)]}
            for k2, v2 in new_card.items():
                k = k2
                v = v2
    for key in new_card:
        st.session_state.given_cards[key] += [new_card[key]]
    return new_card

def deal():
    st.session_state.dealer_cards.append(hit())
    st.session_state.dealer_cards.append(hit())
    st.session_state.player_cards.append(hit())
    st.session_state.player_cards.append(hit())

# Initialize session state
def initialize_game():
    st.session_state.given_cards = {HEARTS: [], DIAMONDS: [], SPADES: [], CLUBS: []}
    st.session_state.dealer_cards = []
    st.session_state.player_cards = []
    st.session_state.hide_card = True
    st.session_state.player_bj = ''
    st.session_state.dealer_bj = ''
    st.session_state.game_over = False
    st.session_state.message = ''
    deal()

if 'given_cards' not in st.session_state:
    initialize_game()

def get_points(cards, hidden=False):
    points = 0
    aces = 0
    start = 0
    if hidden:
        start = 1
    for item in range(start, len(cards)):
        for k, v in cards[item].items():
            if v in ['J', 'Q', 'K']:
                v = 10
            elif v == 'A':
                v = 1
                aces += 1
            points += v
    while points <= 11 and aces > 0:
        points += 10
        aces -= 1
    return points

def show_cards(cards, hidden=False):
    row1, row2, row3, row4, row5, row6 = [], [], [], [], [], []
    start = 0
    if hidden:
        row1.append(' _______ ')
        row2.append("|       |")
        row3.append("| ##### |")
        row4.append("| ##### |")
        row5.append("| ##### |")
        row6.append("'_______'")
        start = 1
    for item in range(start, len(cards)):
        for k, v in cards[item].items():
            if v == 10:
                row1.append(' _______ ')
                row2.append("|       |")
                row3.append(f"| {v}    |")
                row4.append(f"|   {k}   |")
                row5.append(f"|    {v} |")
                row6.append("'_______'")
            else:
                row1.append(' _______ ')
                row2.append("|       |")
                row3.append(f"| {v}     |")
                row4.append(f"|   {k}   |")
                row5.append(f"|     {v} |")
                row6.append("'_______'")

    card_image = "\n".join([
        " ".join(row1),
        " ".join(row2),
        " ".join(row3),
        " ".join(row4),
        " ".join(row5),
        " ".join(row6)
    ])
    
    st.code(card_image, language='text')

def check_game_status():
    dealer_points = get_points(st.session_state.dealer_cards, st.session_state.hide_card)
    player_points = get_points(st.session_state.player_cards)
    if (player_points == 21) and (len(st.session_state.player_cards) == 2):
        st.session_state.hide_card = False
        st.session_state.player_bj = 'BLACKJACK !!!'
    if (dealer_points == 21) and (len(st.session_state.dealer_cards) == 2):
        st.session_state.dealer_bj = 'BLACKJACK !!!'
    if (dealer_points > 21) or ((player_points > dealer_points) and not st.session_state.hide_card) or (st.session_state.player_bj and not st.session_state.dealer_bj):
        st.session_state.message = "** YOU WON !! :) **"
        st.session_state.game_over = True
    elif (player_points > 21) or ((dealer_points > 17) and (dealer_points > player_points) and not st.session_state.hide_card) or (st.session_state.dealer_bj and not st.session_state.player_bj):
        st.session_state.message = "** YOU LOST :( **"
        st.session_state.game_over = True
    elif (dealer_points > 17) and (dealer_points == player_points) and not st.session_state.hide_card:
        st.session_state.message = "** DRAW :| **"
        st.session_state.game_over = True

def reset_game():
    initialize_game()

dealer_points = get_points(st.session_state.dealer_cards, st.session_state.hide_card)
player_points = get_points(st.session_state.player_cards)
check_game_status()

st.write(f"Dealer: {dealer_points} {st.session_state.dealer_bj}")
show_cards(st.session_state.dealer_cards, st.session_state.hide_card)
st.write(f"\nPlayer: {player_points} {st.session_state.player_bj}")
show_cards(st.session_state.player_cards)

# Adding unique keys to buttons to force rerun
if not st.session_state.game_over:
    col1, col2, col3 = st.columns([1, 1, 7], gap="small")
    with col1:
        if st.button("Hit", key="hit"):
            st.session_state.player_cards.append(hit())
            check_game_status()
            st.rerun()
    with col2:
        if st.button("Stand", key="stand"):
            st.session_state.hide_card = False
            dealer_points = get_points(st.session_state.dealer_cards, st.session_state.hide_card)
            while dealer_points < 17:
                st.session_state.dealer_cards.append(hit())
                check_game_status()
                st.rerun()
                time.sleep(1)
    with col3:
        pass

st.write(st.session_state.message)

if st.session_state.game_over and st.button("Play again", key="play_again"):
    reset_game()
    st.rerun()
