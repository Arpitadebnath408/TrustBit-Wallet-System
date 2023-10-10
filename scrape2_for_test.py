import requests
from bs4 import BeautifulSoup

# Replace this with the Bitcoin address you want to look up
bitcoin_address = '1EMdhZCYddTiFfr1hhrxEpx9LFTihekJ73'

# URL for the blockchain.com address lookup page
url = f'https://www.blockchain.com/btc/address/{bitcoin_address}'

# Send an HTTP GET request to the URL
res = requests.get(url)

# Initialize variables with default values
bitcoin_balance_btc = 0
bitcoin_balance_usd = 0
total_received_btc = 0
total_received_usd = 0
total_sent_btc = 0
total_sent_usd = 0
total_volume = 0
transactions = 0

# Check if the request was successful
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the Bitcoin balance in BTC and USD
    try:
        bitcoin_balance_btc = soup.find('div', class_='sc-1g6z2tq-0 cQxRmm').text.strip()
        bitcoin_balance_usd = soup.find('div', class_='sc-1g6z2tq-0 hDSaKM').text.strip()
    except AttributeError:
        pass

    # Find other relevant information (total received, total sent, transactions)
    transaction_summary = soup.find_all('div', class_='sc-10hgmud-2 hneolp')

    try:
        total_received_btc = transaction_summary[0].text.strip()
        total_received_usd = transaction_summary[1].text.strip()
        total_sent_btc = transaction_summary[2].text.strip()
        total_sent_usd = transaction_summary[3].text.strip()
        total_volume = transaction_summary[4].text.strip()
        transactions = transaction_summary[5].text.strip()
    except (IndexError, AttributeError):
        pass

# Print the extracted data
print(f'Bitcoin Balance (BTC): {float(bitcoin_balance_btc)}')
print(f'Bitcoin Balance (USD): {float(bitcoin_balance_usd)}')
print(f'Total Received (BTC): {float(total_received_btc)}')
print(f'Total Received (USD): {float(total_received_usd)}')
print(f'Total Sent (BTC): {float(total_sent_btc)}')
print(f'Total Sent (USD): {float(total_sent_usd)}')
print(f'Total Volume (BTC): {float(total_volume)}')
print(f'Transactions: {float(transactions)}')
