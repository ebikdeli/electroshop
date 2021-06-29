from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Order


@login_required
def orders_all(request, username=None):
    user = User.objects.get(username=username)
    if user.is_staff:
        orders = Order.objects.all()
        return render(request, 'order_all.html', {'orders': orders})
