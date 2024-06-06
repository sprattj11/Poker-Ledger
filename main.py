import pandas as pd

def generate_poker_ledger(input_file):
    # Read input CSV file
    df = pd.read_csv(input_file)

    # Convert net column to dollars with two decimal places
    df['net'] = df['net'] / 100

    # Combine nets for players with the same name
    condensed = df.groupby('player_nickname')['net'].sum().reset_index()

    # Separate winners and losers
    winners = condensed[condensed['net'] > 0].sort_values('net', ascending=False)
    losers = condensed[condensed['net'] < 0].sort_values('net', ascending=True)

    # Iterate through losers and redistribute their net amounts to winners
    for loser_index, loser_row in losers.iterrows():
        remaining_payment = -loser_row['net']  # Amount the loser owes
        for winner_index, winner_row in winners.iterrows():
            if winner_row['net'] <= 0:
                continue
            payment = min(remaining_payment, winner_row['net'], abs(loser_row['net']))  # Calculate payment
            print(f"{loser_row['player_nickname']} pays {winner_row['player_nickname']} ${payment:.2f}")
            winners.at[winner_index, 'net'] -= payment
            remaining_payment -= payment
            if remaining_payment == 0:
                break

# Example usage:
input_file = "ledger.csv"
generate_poker_ledger(input_file)
