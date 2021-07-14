from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from django.contrib.auth.views import auth_login
from profile.models import Profile
from profile.forms import ProfileEditForm, EmailUserForm,\
    ProfileCreateForm, UserCreateForm, UserAuthenticationLoginForm
import re

"""
def profile_login(request):
    if request.method == 'POST':
        user_auth_form = UserAuthenticationLoginForm(request.POST)
        if user_auth_form.is_valid():
            user_auth = user_auth_form.cleaned_data
            user = authenticate(request, username=user_auth['username'], password=user_auth['password'])
            if user is not None:
                login(request, user)
                return redirect('shop:index')
            messages.add_message(request, messages.ERROR, 'username or password is wrong!')
    else:
        user_auth_form = UserAuthenticationLoginForm()

    return render(request, 'profile_login.html', {'user_auth_form': user_auth_form})
"""


def user_login_signup(request):
    if request.method == 'POST':
        user_create_form = UserCreateForm()
        user_auth_form = UserAuthenticationLoginForm()

    else:
        print('before form')
        user_create_form = UserCreateForm()
        user_auth_form = UserAuthenticationLoginForm()

    return render(request, 'profile/templates/profile_login.html', context={
        'user_create_form': user_create_form,
        'user_auth_form': user_auth_form,
    })


def user_signup(request):
    if request.method == 'POST':
        user_create_form = UserCreateForm(data=request.POST)
        if user_create_form.is_valid():
            pass
    else:
        return redirect('profile:login_signup')


def user_login(request):
    if request.method == 'POST':

        user_auth_form = UserAuthenticationLoginForm(data=request.POST)
        print(user_auth_form)
        if user_auth_form.is_valid():
            user_auth = user_auth_form.cleaned_data
            user = authenticate(request, username=user_auth['username_or_email_login'], password=user_auth['password'])
            if user is not None:
                login(request, user)
                return redirect('shop:index')
            try:
                user = User.objects.get(email=user_auth['username_or_email_login'])
                login(request, user)
                return redirect('shop:index')
            except User.DoesNotExist:
                print('user not exist!')
                messages.add_message(request, messages.ERROR, 'اطلاعات وارد شده اشتباه است!')
    else:
        return redirect('profile:login_signup')


def profile_login(request):
    pass


@login_required
def profile_view(request, username=None):
    return render(request, 'profile/templates/profile_view.html')


@login_required
def profile_edit(request, username):
    initial_profile_form_data = {
        'phone': Profile.phone,
        'address': Profile.address,
        'picture': Profile.picture,
    }
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if request.method == 'POST':
        profile_edit_form = ProfileEditForm(data=request.POST, files=request.FILES)
        email_form = EmailUserForm(data=request.POST)
        if profile_edit_form.is_valid() and email_form.is_valid():
            current_user = User.objects.get(username=username)
            current_user.email = email_form.cleaned_data['email']
            try:
                current_profile = current_user.profile
                current_profile.phone = profile_edit_form.cleaned_data['phone']
                current_profile.address = profile_edit_form.cleaned_data['address']
                current_profile.picture = profile_edit_form.cleaned_data['picture']
            except Profile.DoesNotExist:
                current_profile = Profile.objects.create(user=current_user,
                                                         phone=profile_edit_form.cleaned_data['phone'],
                                                         address=profile_edit_form.cleaned_data['address'],
                                                         picture=profile_edit_form.cleaned_data['picture'])
            current_profile.save()
            current_user.save()
            Cart.objects.create(profile=current_profile)
            return redirect('shop:index')

    else:
        try:
            request.user.profile
            profile_edit_form = ProfileEditForm(initial=initial_profile_form_data)
        except Profile.DoesNotExist:
            profile_edit_form = ProfileEditForm()
        # email_form = EmailUserForm({'email': username}) if re.search(email_regex, username) else EmailUserForm()
        if User.objects.get(username=username).email:
            email_form = EmailUserForm({'email': User.objects.get(username=username).email})
        else:
            email_form = EmailUserForm()

    return render(request, 'profile/templates/profile_edit.html', context={'profile_edit_form': profile_edit_form,                                                                           'email_form': email_form})


@login_required
def user_logout(request, username=None):
    logout(request)
    return redirect('shop:index')
