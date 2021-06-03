from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, 'social_login/templates/login.html')


@login_required
def home(request):
    return render(request, 'social_login/templates/home.html')
