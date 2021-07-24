from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
# from django.contrib.auth.views import auth_login
from cart.models import Cart
from profile.models import Profile
from profile.forms import ProfileEditForm, UserEmailNameForm,\
    ProfileCreateForm, UserCreateForm, UserAuthenticationLoginForm
# import re

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
            try:
                new_user = User.objects.create(
                    username=user_create_form.cleaned_data['username'],
                    password=user_create_form.cleaned_data['password1'],
                    email=user_create_form.cleaned_data['email']
                )
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'نام کاربری مورد نظر شما قبلا ثبت شده')
                return redirect('profile:login_signup')

            new_profile = Profile.objects.create(user=new_user)
            try:
                Cart.objects.create(profile=new_profile)
            except IntegrityError:
                # Cart.objects.get(profile=new_profile)
                pass

            login(request, new_user,  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile:profile_view', username=new_user.username)

        else:
            messages.add_message(request, messages.ERROR, 'اطلاعات را به درستی وارد کنید')
            return redirect('profile:login_signup')


def user_login(request):
    if request.method == 'POST':
        user_auth_form = UserAuthenticationLoginForm(data=request.POST)

        if user_auth_form.is_valid():
            user_auth = user_auth_form.cleaned_data
            print(user_auth)
# user = authenticate(request, username=user_auth['username_or_email_login'], password=user_auth['password'])
            user = User.objects.get(username=user_auth['username_or_email_login'], password=user_auth['password'])
            print(user)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('shop:index')

            try:
                user = User.objects.get(email=user_auth['username_or_email_login'])
                login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
                return redirect('shop:index')

            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'اطلاعات وارد شده اشتباه است!')
                return redirect('profile:login_signup')
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
    # email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if request.method == 'POST':
        profile_edit_form = ProfileEditForm(data=request.POST, files=request.FILES)
        user_email_name_form = UserEmailNameForm(data=request.POST)
        print('error: ', user_email_name_form.errors, '  ', profile_edit_form.errors)
        if profile_edit_form.is_valid() and user_email_name_form.is_valid():
            current_user = User.objects.get(username=username)
            current_user.first_name = user_email_name_form.cleaned_data['first_name']
            current_user.last_name = user_email_name_form.cleaned_data['last_name']
            current_user.email = user_email_name_form.cleaned_data['email']
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
            print('all saved')
            try:
                Cart.objects.get(profile=current_profile)
            except Cart.DoesNotExist:
                Cart.objects.create(profile=current_profile)

            return redirect('profile:profile_view', username=current_user.username)

    else:
        try:
            request.user.profile
            profile_edit_form = ProfileEditForm(initial=initial_profile_form_data)
        except Profile.DoesNotExist:
            profile_edit_form = ProfileEditForm()
        # email_form = EmailUserForm({'email': username}) if re.search(email_regex, username) else EmailUserForm()
        user = User.objects.get(username=username)

        user_email_name_form = UserEmailNameForm(initial={
                'email': user.email if user.email else '',
                'first_name': user.first_name if user.first_name else '',
                'last_name': user.last_name if user.last_name else ''
            })
        """
        else:
            user_email_name_form = UserEmailNameForm()
        """

    return render(request, 'profile/templates/profile_edit.html', context={'profile_edit_form': profile_edit_form,
                                                                           'email_form': user_email_name_form})


@login_required
def user_logout(request, username=None):
    logout(request)
    return redirect('shop:index')
