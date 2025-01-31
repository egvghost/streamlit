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
import streamlit as st

blackjack_logo = '''
.--------.            _     _            _    _            _    
| A_  _  |           | |   | |          | |  (_)          | |   
| ( \/ ).--------.   | |__ | | __ _  ___| | ___  __ _  ___| | __
|  \  / | K /\   |   | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|   \/ A|  /  \  |   | |_) | | (_| | (__|   <| | (_| | (__|   < 
'-------|  \  /  |   |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\ 
        |   \/ K |                          _/ |                
        '--------'                         |__/                 

'''

# Set up the constants:
HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.

numbers = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
suits = [HEARTS, DIAMONDS, SPADES, CLUBS]

dealer_cards = []
player_cards = []
given_cards = {HEARTS: [], DIAMONDS: [], SPADES: [], CLUBS: []}

def hit():
    new_card = {suits[random.randint(0, 3)]: numbers[random.randint(0, 12)]}
    # Avoid card duplicates
    for k, v in new_card.items():
        while v in given_cards[k]:
            new_card = {suits[random.randint(0, 3)]: numbers[random.randint(0, 12)]}
            for k2, v2 in new_card.items():
                k = k2
                v = v2
    # Register given cards to avoid duplicates
    for key in new_card:
        given_cards[key] += [new_card[key]]
    return new_card

def deal():
    dealer_cards.append(hit())
    dealer_cards.append(hit())
    player_cards.append(hit())
    player_cards.append(hit())
    return player_cards, dealer_cards

def show_cards(cards, hidden=False):
    rows = [[], [], [], [], [], []]
    start = 0
    if hidden:
        rows[0].append(' _______ ')
        rows[1].append("|       |")
        rows[2].append("| ##### |")
        rows[3].append("| ##### |")
        rows[4].append("| ##### |")
        rows[5].append("'_______'")
        start = 1
    for item in range(start, len(cards)):
        for k, v in cards[item].items():
            if v == 10:
                rows[0].append(' _______ ')
                rows[1].append("|       |")
                rows[2].append(f"| {v}    |")
                rows[3].append(f"|   {k}   |")
                rows[4].append(f"|    {v} |")
                rows[5].append("'_______'")
            else:
                rows[0].append(' _______ ')
                rows[1].append("|       |")
                rows[2].append(f"| {v}     |")
                rows[3].append(f"|   {k}   |")
                rows[4].append(f"|     {v} |")
                rows[5].append("'_______'")
    for row in rows:
        st.write(" ".join(row))

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
            else:
                pass
            points += v
        # Change aces value from '1' to '11' if convenient
    if points <= 11 and aces > 0:
        points += 10
    return points

def main():
    logo_placeholder = st.empty()
    dealer_placeholder = st.empty()
    player_placeholder = st.empty()
    result_placeholder = st.empty()
    while True:
        given_cards = {HEARTS: [], DIAMONDS: [], SPADES: [], CLUBS: []}
        hide_card = True
        dealer_cards = []
        player_cards = []
        player_bj = ''
        dealer_bj = ''
        deal()
        while True:
            logo_placeholder.write(blackjack_logo)
            dealer_points = get_points(dealer_cards, hide_card)
            player_points = get_points(player_cards)
            if (player_points == 21) and (len(player_cards) == 2):
                hide_card = False
                player_bj = 'BLACKJACK !!!'
            if (dealer_points == 21) and (len(dealer_cards) == 2):
                dealer_bj = 'BLACKJACK !!!'
            dealer_placeholder.write(f"Dealer: {dealer_points} {dealer_bj}")
            show_cards(dealer_cards, hide_card)
            player_placeholder.write(f"\nPlayer: {player_points} {player_bj}")
            show_cards(player_cards)
            if (dealer_points > 21) or ((player_points > dealer_points) and not hide_card) or (player_bj and not dealer_bj):
                result_placeholder.write("\n** YOU WON !! :) **")
                break
            elif (player_points > 21) or ((dealer_points > player_points) and not hide_card) or (dealer_bj and not player_bj):
                result_placeholder.write("\n** YOU LOST :( **")
                break
            elif (dealer_points == player_points) and not hide_card:
                result_placeholder.write("\n** DRAW :| **")
                break
            else:
                player_choice = st.radio("Choose your move", ["(H)it", "(S)tand"], index=None, key=random.randint(0, 9999)) 
                if player_choice == "(H)it":
                    player_cards.append(hit())
                elif player_choice == "(S)tand":
                    hide_card = False
                    dealer_points = get_points(dealer_cards, hide_card)
                    while dealer_points < 17:
                        dealer_cards.append(hit())
                        dealer_points = get_points(dealer_cards, hide_card)
        keep_playing = st.radio("\nPlay again?", ["Yes", "No"], index=None, key=random.randint(0, 9999)) 
        if keep_playing.lower() == 'no':
            break

if __name__ == '__main__':
    main()
