import pandas as pd
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    # Replace with your email provider's SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "warriorhawk2003@gmail.com"
    password = "itic ewkv azad zkvr "

    msg = MIMEText(body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

def generate_poker_ledger(input_file, to_phone_email):
    df = pd.read_csv(input_file)
    df['net'] = df['net'] / 100
    condensed = df.groupby('player_nickname')['net'].sum().reset_index()
    winners = condensed[condensed['net'] > 0].sort_values('net', ascending=False)
    losers = condensed[condensed['net'] < 0].sort_values('net', ascending=True)

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

    body = "\n\n".join(output)
    send_email("Poker Ledger Payment", body, to_phone_email)

# Example usage:
input_file = "ledger.csv"
to_phone_email = "7029940967@txt.att.net"  # Replace with your carrier's email-to-SMS gateway
generate_poker_ledger(input_file, to_phone_email)
