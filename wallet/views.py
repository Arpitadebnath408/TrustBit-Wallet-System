from django.shortcuts import render, redirect
from users.models import UserInfo
from .models import *
import bs4
import requests
from django.contrib import messages
from messaging.models import *

def index(request):
    user = request.user  # Get the user object
    
    # API endpoint for CoinGecko
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    
    # Parameters for the API request
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    
    bitcoin_price = 0
    
    try:
        # Send a GET request to the CoinGecko API
        response = requests.get(api_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            bitcoin_price = data["bitcoin"]["usd"]
            print(f"Live Bitcoin Price: {bitcoin_price:.2f} USD")
        else:
            print("Failed to retrieve data from the API.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    live_bitcoin_price = float(bitcoin_price)
    
    # Check if the user is authenticated (logged in)
    if user.is_authenticated:
        user_info = UserInfo.objects.get(user=user)
        messages = Message.objects.filter(receiver=user_info)
        unread_count = 0
        if messages:
            unread_count = messages.filter(is_read=False).count()
        if request.method == 'POST':
            addr = request.POST['addr']

            res = requests.get('https://www.blockchain.com/btc/address/'+addr)
            bitcoin_balance_btc = 0
            bitcoin_balance_usd = 0
            total_received_btc = 0
            total_received_usd = 0
            total_sent_btc = 0
            total_sent_usd = 0
            transactions = 0
            if res:
                soup = bs4.BeautifulSoup(res.text, 'html.parser')
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
                    transactions = transaction_summary[5].text.strip()
                except (IndexError, AttributeError):
                    pass
                
                bitcoin_balance_btc = float(bitcoin_balance_btc)
                bitcoin_balance_usd = float(bitcoin_balance_usd)
                total_received_btc = float(total_received_btc)
                total_received_usd = float(total_received_usd)
                total_sent_btc = float(total_sent_btc)
                total_sent_usd = float(total_sent_usd)
                live_bitcoin_price = float(live_bitcoin_price)
                balance_usd = bitcoin_balance_usd * live_bitcoin_price
                total_received_usd = total_received_usd * live_bitcoin_price
                total_sent_usd = total_sent_usd * live_bitcoin_price
            else:
                return redirect('index')
    
            try:
                # Retrieve the associated UserInfo and UserWalletDetails
                user_info = UserInfo.objects.get(user=user)
                # Retrieve the UserWalletDetails using the private_key from UserInfo
                user_wallet_details = UserWalletDetails.objects.get(private_key=user_info.private_key)
                user_wallet_details.balance = bitcoin_balance_btc
                user_wallet_details.balance1 = total_received_usd
                user_wallet_details.transactions = transactions
                user_wallet_details.total_received = total_sent_btc
                user_wallet_details.total_received1 = total_sent_usd
                user_wallet_details.total_sent = total_sent_btc
                user_wallet_details.total_sent1 = total_sent_usd
                user_wallet_details.live_bitcoin_price = live_bitcoin_price
                user_wallet_details.balance_usd = int(balance_usd)
                user_wallet_details.total_received_usd = int(total_received_usd)
                user_wallet_details.total_sent_usd = int(total_sent_usd)
            except UserInfo.DoesNotExist:
                # Handle the case where UserInfo does not exist for the user
                user_info = None
                user_wallet_details = None
            except UserWalletDetails.DoesNotExist:
                # Handle the case where UserWalletDetails does not exist for the given private_key
                user_wallet_details = None

            return render(request, "index.html", {'user': user, 'user_info': user_info, 'user_wallet_details': user_wallet_details, 'live_bitcoin_price': live_bitcoin_price})
        else:
            try:
                # Retrieve the associated UserInfo and UserWalletDetails
                user_info = UserInfo.objects.get(user=user)
                # Retrieve the UserWalletDetails using the private_key from UserInfo
                user_wallet_details = UserWalletDetails.objects.get(private_key=user_info.private_key)
            except UserInfo.DoesNotExist:
                # Handle the case where UserInfo does not exist for the user
                user_info = None
                user_wallet_details = None
            except UserWalletDetails.DoesNotExist:
                # Handle the case where UserWalletDetails does not exist for the given private_key
                user_wallet_details = None

            return render(request, "index.html", {'user': user, 'user_info': user_info, 'user_wallet_details': user_wallet_details, 'live_bitcoin_price': live_bitcoin_price, 'unread_count': unread_count})
    else:
        # User is not authenticated
        return render(request, "index.html", {'live_bitcoin_price': live_bitcoin_price})
    
def about(request):
    user = request.user  # Get the user object
    user_info = UserInfo.objects.get(user=user)
    messages = Message.objects.filter(receiver=user_info)
    unread_count = 0
    if messages:
        unread_count = messages.filter(is_read=False).count()
    return render(request, "about.html", {'unread_count': unread_count})
    
def submit_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')

        submission = FormSubmission(email=email, name=name, message=message)
        submission.save()

        messages.success(request, 'Form submitted successfully!')
        return redirect('index')

    return render(request, 'index.html')

def send_bitcoin(request):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    messages = Message.objects.filter(receiver=user_info)
    unread_count = 0
    if messages:
        unread_count = messages.filter(is_read=False).count()
    return render(request, "send_bitcoin.html", {"user_info": user_info, "unread_count": unread_count})

def receive_bitcoin(request):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    messages = Message.objects.filter(receiver=user_info)
    unread_count = 0
    if messages:
        unread_count = messages.filter(is_read=False).count()
    return render(request, "receive_bitcoin.html", {"user_info": user_info, "unread_count": unread_count})