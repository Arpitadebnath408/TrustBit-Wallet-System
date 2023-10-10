from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserInfo
from wallet.models import UserWalletDetails
from bitcoin import *

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials. Please try again')
            return redirect('login')
    else:
        return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password==password2:       
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Taken. Please try again with another email')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken. Please try again with another username')
                return redirect('register')
            else:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                print('User Created')
                private_key = random_key()
                public_key = privtopub(private_key)
                address = pubtoaddr(public_key)
                # Create the user info with keys and address
                user_info = UserInfo.objects.create(
                    user=user,
                    public_key=public_key,
                    private_key=private_key,
                    address=address
                )
                user_info.save()
                # Create the user wallet details with keys and address
                user_wallet_detail = UserWalletDetails.objects.create(
                    public_key=public_key,
                    private_key=private_key,
                    address=address
                )
                user_wallet_detail.save()
                
                messages.info(request, 'Registration successful. Please log in.')
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching. Please try again')
            return redirect('register')
        
    return render(request, "register.html")

def logout(request):
    request.session.clear()
    return redirect("index")