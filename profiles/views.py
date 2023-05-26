from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import modelformset_factory
from .models import Profile, ProfileImage
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm, ProfileImageForm, EditProfileForm, MessagesForm
from chat.models import Conversations, Messages, Views
from django.views.decorators.csrf import csrf_protect
import stripe
import datetime
import time
import os

# Регистрация нового пользователя
def register(request):
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                user_reg = User.objects.get(username=user)
                profile = Profile(user=user_reg)
                profile.save()
                messages.success(request, "Аккаунт был успешно создаан")
                auth.login(user=user_reg, request=request)
                return redirect('create_profile')
            else:
                messages.error(request, "Невозможно создать аккаунт")
    else:
        registration_form = UserRegistrationForm()
    context = {
        'registration_form':registration_form
    }
    return render(request, 'register.html', context)

# Авторизация
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                messages.success(request, "Logged in successfully")
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else:
                messages.error(request, "Username or password incorrect")
    else:
        login_form = UserLoginForm()

    context = {
        'login_form':login_form
    }
    return render(request, 'login.html', context)

# Профиль пользователя
# Если открывается страница авторизованного пользователя - страница с данными
# Иначе добавляется еще форма для сообщений
@login_required
def member_profile(request, id):
    member = User.objects.get(id=id)
    height = str(member.profile.height)
    if not member == request.user:
        current_user = False
        last_view = Views.objects.filter(receiver_id=id).filter(sender_id=request.user.id).last()
        if not last_view or last_view.is_read:
            view = Views(receiver=member, sender=request.user)
            view.save()
        if request.method == "POST" and 'message_submit' in request.POST:
            message_form = MessagesForm(request.POST)
            if message_form.is_valid():
                print(7)
                conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=id)
                if conversation.exists():
                    message = message_form.save(commit=False)
                    message.sender = request.user
                    message.receiver = User.objects.get(pk=id)
                    message.conversation = conversation[0]
                    message.save()
                    return redirect('/chat/%s' % conversation[0].id )
                else:
                    receiver = User.objects.get(pk=id)
                    conversation = Conversations()
                    conversation.save()
                    conversation.participants.add(request.user.id)
                    conversation.participants.add(receiver)
                    message = message_form.save(commit=False)
                    message.sender = request.user
                    message.receiver = receiver
                    message.conversation = conversation
                    message.save()
                    return redirect('/chat/%s' % conversation.id )
        else:
            message_form = MessagesForm()
    else:
        message_form = MessagesForm()
        current_user = True
    context = {
        'height': height,
        'member':member,
        'message_form': message_form,
        'current_user': current_user
    }
    return render(request, 'member.html', context)

# Выход из аккаунта
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "Вы вышли из аккаунта.")
    return redirect(reverse('preregister'))

# Создание/редактирование профиля пользователя
@login_required
def create_profile(request):
    ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=6, max_num=6, help_texts=None)
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES)

        formset = ImageFormSet(request.POST, request.FILES,
                              queryset=ProfileImage.objects.filter(user_id=request.user.id).all())

        if profile_form.is_valid() and formset.is_valid():
            instance = profile_form.save(commit=False)
            instance.user_id = request.user.id
            instance.save()

            for form in formset:
                if form.is_valid() and form.has_changed():
                    instance_image = form.save(commit=False)
                    instance_image.user = request.user
                    instance_image.save()

            return redirect(reverse('verification_message'))

    else:
        profile_form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        initial_images = [{'image_url': i.image} for i in ProfileImage.objects.filter(user_id=request.user.id).all() if i.image]
        formset = ImageFormSet(queryset=ProfileImage.objects.filter(user_id=request.user.id).all(), initial=initial_images)

    context = {
        'profile_form':profile_form,
        'image_form':image_form,
        'formset': formset
    }
    return render(request, 'create-profile.html', context)

# Верификация измененных данных пользователя
def verification_message(request):
    return render(request, 'verification-message.html')

# Изменение пароля, адреса электронной почты и логина
@login_required
def account(request):
    if request.method == "POST" and 'account-change-submit' in request.POST:
        password_form = PasswordChangeForm(request.user)
        user_form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if user_form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user_form.save()
            user = User.objects.get(pk=request.user.id)
        else:
            user = User.objects.get(pk=request.user.id)
            request.user = user
    elif request.method == "POST" and 'password-change-submit' in request.POST:
            user_form = EditProfileForm(instance=request.user, user=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
    else:
        user_form = EditProfileForm(instance=request.user, user=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'password_form': password_form,
        'user_form': user_form,
    }
    return render(request, 'account.html', context)
