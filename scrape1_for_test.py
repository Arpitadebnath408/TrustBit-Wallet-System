import requests
from bs4 import BeautifulSoup

# URL of the website containing the Bitcoin price
url = "https://www.coindesk.com/coindesk20"

try:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the Bitcoin price element
        bitcoin_price_element = soup.find('span', class_='price-values')

        # Extract the price text and remove the dollar sign and commas, replace period with empty string
        bitcoin_price_text = bitcoin_price_element.text.strip().replace('$', '').replace(',', '').replace('.', '')

        # Convert the price to a floating-point value
        bitcoin_price_float = float(bitcoin_price_text) / 100  # Divide by 100 to account for cents

        # Print the live Bitcoin price as a floating-point value
        print(f"Live Bitcoin Price: {bitcoin_price_float:.2f}")  # Display up to 2 decimal places
    else:
        print("Failed to retrieve data from the website.")
except Exception as e:
    print(f"An error occurred: {e}")

# Using api
# import requests

# # API endpoint for CoinGecko
# api_url = "https://api.coingecko.com/api/v3/simple/price"

# # Parameters for the API request
# params = {
#     "ids": "bitcoin",
#     "vs_currencies": "usd"
# }

# try:
#     # Send a GET request to the CoinGecko API
#     response = requests.get(api_url, params=params)

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         bitcoin_price = data["bitcoin"]["usd"]
#         print(f"Live Bitcoin Price: {bitcoin_price:.2f} USD")
#     else:
#         print("Failed to retrieve data from the API.")
# except Exception as e:
#     print(f"An error occurred: {e}")
