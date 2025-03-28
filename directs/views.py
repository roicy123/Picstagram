from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Message
from authy.models import Profile  # Adjust import based on your project structure

@login_required
def inbox(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    messages_list = Message.get_message(user=user)
    active_direct = None
    directs = None

    if messages_list:
        message = messages_list[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True, status='delivered')

        for msg in messages_list:
            if msg['user'].username == active_direct:
                msg['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages_list,
        'active_direct': active_direct,
        'profile': profile,
    }
    return render(request, 'directs/direct.html', context)

@login_required
def Directs(request, username):
    user = request.user
    messages_list = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True, status='seen')

    for message in messages_list:
        if message['user'].username == username:
            message['unread'] = 0
    
    context = {
        'directs': directs,
        'messages': messages_list,
        'active_direct': active_direct,
    }
    return render(request, 'directs/direct.html', context)

@login_required
def SendDirect(request):
    if request.method == "POST":
        to_user_username = request.POST.get('to_user')
        body = request.POST.get('body', '')
        file = request.FILES.get('file')

        try:
            to_user = User.objects.get(username=to_user_username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('message')

        # Determine message type
        message_type = 'text'
        if file:
            content_type = file.content_type
            if content_type.startswith('image/'):
                message_type = 'image'
            elif content_type.startswith('video/'):
                message_type = 'video'
            elif content_type.startswith('audio/'):
                message_type = 'voice'
            else:
                message_type = 'file'

        # Use the static method to create messages
        Message.sender_message(
            request.user, 
            to_user, 
            body, 
            file=file, 
            message_type=message_type
        )

        messages.success(request, "Message sent successfully.")
        return redirect('message')

def UserSearch(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
    else:
        users_paginator = []

    context = {
        'users': users_paginator,
    }
    return render(request, 'directs/search.html', context)

def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('search-users')
    
    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
    
    return redirect('message')