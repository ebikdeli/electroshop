from django import forms
from django.contrib.auth.forms import UserCreationForm
from profile.models import Profile


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'picture']


class UserCreateForm(UserCreationForm):
    email = forms.EmailField()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'picture', ]


class EmailUserForm(forms.Form):
    email = forms.EmailField()


class UserAuthenticationLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
