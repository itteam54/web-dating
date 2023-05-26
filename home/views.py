from django.shortcuts import render
from django.db.models import Q, F
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from chat.models import Conversations
from profiles.models import Profile, ProfileImage
import datetime as DT

# Главная для авторизованных пользователей
@login_required
def postregister(request):
    card_profiles = Profile.objects.order_by('location').filter(Q(looking_for=request.user.profile.gender)).filter(gender=request.user.profile.looking_for).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).all()[:10]

    if card_profiles.count() == 0:
        card_profiles_exists = False
    else:
        card_profiles_exists = True

    context = {
        'card_profiles_exists' : card_profiles_exists,
        'card_profiles': card_profiles
    }

    return render(request, 'home.html')#, context)

# Домашняя для неавторизованных пользователей
def preregister(request):
    return render(request, 'index.html')
