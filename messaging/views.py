from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from users.models import UserInfo
from django.db.models import Q
from django.db.models import Max

@login_required
def send_message(request):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    messages = Message.objects.filter(receiver=user_info)
    unread_count = 0
    if messages:
        unread_count = messages.filter(is_read=False).count()
        
    if request.method == 'POST':
        user_address = request.POST.get('user_address')
        receiver_address = request.POST.get('receiver_address')
        message_text = request.POST.get('message_text')

        try:
            sender = UserInfo.objects.get(address=user_address)
            receiver = UserInfo.objects.get(address=receiver_address)
            message = Message(sender=sender, receiver=receiver, message=message_text)
            message.save()
            return render(request, 'send_message.html', {"user_info": user_info, "msg": "Message has sent successfully", "unread_count": unread_count})
        except UserInfo.DoesNotExist:
            return render(request, 'send_message.html', {"user_info": user_info, "error_msg": "Error! Please try again.", "unread_count": unread_count})

    return render(request, 'send_message.html', {"user_info": user_info, "unread_count": unread_count})

@login_required
def messages(request):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    messages = Message.objects.filter(receiver=user_info)
    
    # Get the latest message for each conversation partner
    conversations = Message.objects.filter(Q(sender=user_info) | Q(receiver=user_info)).values('sender', 'receiver').annotate(last_message=Max('timestamp'))
    # Create a dictionary to store conversation partners and their latest messages
    conversations_dict = {}
    for conversation in conversations:
        partner_id = conversation['sender'] if conversation['sender'] != user_info.id else conversation['receiver']
        partner = UserInfo.objects.get(id=partner_id)
        last_message = Message.objects.filter(Q(sender=user_info, receiver=partner) | Q(sender=partner, receiver=user_info), timestamp=conversation['last_message']).first()
        conversations_dict[partner] = last_message

    if messages:
        unread_count = messages.filter(is_read=False).count()
        context = {'conversations_dict': conversations_dict, 'messages': messages, 'user_info': user_info, 'unread_count': unread_count}
        return render(request, 'messages.html', context)
    else:
        context = {'conversations_dict': conversations_dict, 'messages': messages, 'user_info': user_info, 'unread_count': 0}
        return render(request, 'messages.html', context)

@login_required
def chat(request, receiver_address):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    receiver = UserInfo.objects.get(address=receiver_address)
    messages = Message.objects.filter(
        (Q(sender=user_info) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=user_info))
    ).order_by('timestamp')
    
    # Mark messages as read
    messages.filter(sender=receiver).update(is_read=True)
    
    msg = Message.objects.filter(sender=receiver).order_by('timestamp')

    unread_count = 0
    if messages:
        unread_count = msg.filter(is_read=False).count()

    context = {'user_info': user_info, 'receiver': receiver, 'messages': messages, 'unread_count': unread_count}
    return render(request, 'chat.html', context)

@login_required
def send_message_api(request, receiver_address):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    
    if request.method == 'POST':
        message_text = request.POST.get('message_text')
        
        try:
            receiver = UserInfo.objects.get(address=receiver_address)
            message = Message(sender=user_info, receiver=receiver, message=message_text, is_read=True)
            message.save()
        except UserInfo.DoesNotExist:
            return JsonResponse({'error_msg': 'Error! Please try again.'})
    
    return JsonResponse({'success_msg': 'Message sent successfully.'})

