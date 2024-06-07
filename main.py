import pandas as pd
import pyperclip

# Copyright 2024 Jason Spratt

# windows specs
# using python 3.12.3 and 3.12.3 interpreter
# using pandas v 2.2.2
# using pyperclip v 1.8.2

# mac specs
# using python 3.12.3 and 3.11.3 interpreter
# using pandas v 2.2.2
# using pyperclip v 1.8.2

def generate_poker_ledger(input_file):

    # read the csv file and condense the info
    df = pd.read_csv(input_file)
    #df['net'] = df['net'] / 100
    condensed = df.groupby('player_nickname')['net'].sum().reset_index()
    winners = condensed[condensed['net'] > 0].sort_values('net', ascending=False)
    losers = condensed[condensed['net'] < 0].sort_values('net', ascending=True)

    # generate the ledger
    output = []
    for loser_index, loser_row in losers.iterrows():
        remaining_payment = -loser_row['net']
        for winner_index, winner_row in winners.iterrows():
            if winner_row['net'] <= 0:
                continue
            payment = min(remaining_payment, winner_row['net'], abs(loser_row['net']))
            output.append(f"{loser_row['player_nickname']} pays {winner_row['player_nickname']} ${payment:.2f}")
            winners.at[winner_index, 'net'] -= payment
            remaining_payment -= payment
            if remaining_payment == 0:
                break

    # copy the ledger to the clipboard
    body = "\n".join(output)
    pyperclip.copy(body)
    print("The ledger has been copied to the clipboard.")

# calling main function
input_file = "ledger.csv"
generate_poker_ledger(input_file)
