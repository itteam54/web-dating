from django.shortcuts import render, reverse, redirect
from .forms import MessageForm, WinkForm
from .models import Conversations, Messages, Winks, Views
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Домашняя страница мессенджера. Показывает только тех, с кем общается пользователь
@login_required
def chat_home(request):
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()
        last_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last()
        if last_message:
            is_read_check[conversation.id] = last_message.is_read
        else:
            is_read_check[conversation.id] = True

    context = {
        'all_conversations': all_conversations,
        'conversation_id': None,
        'is_read_check': is_read_check
    }
    return render(request, 'chat_home.html', context)

# Страница подмигиваний
@login_required
def winks(request, id):
    winks = Winks.objects.filter(receiver=id).order_by('-created_on')
    winks_paginated = Paginator(winks, 3)

    try:
        winks_page = winks_paginated.page(request.GET.get('page'))
    except PageNotAnInteger:
        winks_page = winks_paginated.page(1)
    except EmptyPage:
        winks_page = winks_paginated.page(winks_paginated.num_pages)

    context = {
        'winks_page': winks_page,
    }
    return render(request, 'winks.html', context)

# Подмигнуть пользователю
@login_required
def wink(request, id):
    wink_form = WinkForm()
    wink = wink_form.save(commit=False)
    wink.receiver = User.objects.get(id=id)
    wink.sender = request.user
    wink.save()

    return render(request, 'winked.html')

# Страница просмотров
@login_required
def views(request, id):
    views = Views.objects.filter(receiver=id).order_by('-created_on')
    views_paginated = Paginator(views, 3)
    try:
        views_page = views_paginated.page(request.GET.get('page'))
    except PageNotAnInteger:
        views_page = views_paginated.page(1)
    except EmptyPage:
        views_page = views_paginated.page(views_paginated.num_pages)

    context = {
        'views_page': views_page,
    }
    return render(request, 'views.html', context)

# Переписка с выбранным пользователем
@login_required
def chat(request, id):
    conversation_ids = Conversations.objects.filter(participants=request.user)

    all_conversations = {}
    is_read_check = {}
    for conversation in conversation_ids:
        all_conversations[conversation.id] = Messages.objects.filter(conversation=conversation).last()
        last_message = Messages.objects.filter(conversation=conversation, receiver=request.user).last()
        if last_message:
            is_read_check[conversation.id] = last_message.is_read
        else:
            is_read_check[conversation.id] = True

    messages = Messages.objects.filter(conversation=id).order_by('-created_on')

    conversation = Conversations.objects.get(pk=id)
    participants = conversation.participants.all()
    for user in participants:
        if not user.id == request.user.id:
            receiver = user

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            if receiver.id == request.user.id:
                messages.success(request, "Нельзя переписываться с самим собой")
                return redirect(reverse('chat_home'))

            message = message_form.save(commit=False)
            message.receiver = User.objects.get(id=receiver.id)
            message.sender = request.user
            message.conversation = conversation
            message.save()

            messages_paginated = Paginator(messages, 6)
            try:
                messages_page = messages_paginated.page(request.GET.get('page'))
            except PageNotAnInteger:
                messages_page = messages_paginated.page(1)
            except EmptyPage:
                messages_page = messages_paginated.page(messages_paginated.num_pages)

        context = {
            'user_messages': messages,
            'message_form':message_form,
            'all_conversations': all_conversations,
            'receiver': receiver,
            'conversation_id': int(id),
            'is_read_check': is_read_check
        }

        return redirect(reverse('chat', kwargs={'id':id}))
    else:
        message_form = MessageForm()

        messages_paginated = Paginator(messages, 6)
        try:
            messages_page = messages_paginated.page(request.GET.get('page'))
        except PageNotAnInteger:
            messages_page = messages_paginated.page(1)
        except EmptyPage:
            messages_page = messages_paginated.page(winks_paginated.num_pages)

    context = {
        'user_messages': messages,
        'message_form':message_form,
        'all_conversations': all_conversations,
        'receiver': receiver.id,
        'conversation_id': int(id),
        'is_read_check': is_read_check,
        'messages_page': messages_page
    }
    return render(request, 'chat.html', context)


@login_required
def get_wink(request, id):
    wink_form = WinkForm()
    wink = wink_form.save(commit=False)
    wink.receiver = User.objects.get(id=id)
    wink.sender = request.user
    wink.save()

    return render(request, 'winks.html')
