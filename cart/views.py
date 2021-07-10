from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from profile.models import Profile
from cart.forms import ChangeCart, CouponCode


@login_required
def cart_view(request, username):
    # cart = Profile.objects.get(user=User.objects.get(username=username)).profile_cart
    change_cart_form = ChangeCart()
    context = {'change_cart_form': change_cart_form}
    return render(request, 'cart_view.html', context)


@login_required
def cart_change_item(request, username, item_id=None):
    cart = User.objects.get(username=username).profile.profile_cart
    if request.method == 'POST':
        change_cart_form = ChangeCart(data=request.POST)
        if change_cart_form.is_valid():
            new_quantity = change_cart_form.cleaned_data['quantity']
            if new_quantity == cart.items[item_id]:
                messages.add_message(request, messages.INFO, 'no change happened in the cart')
                return redirect('cart:cart_view', username=username)
            cart.items[item_id] = new_quantity
            cart.save()
            messages.add_message(request, messages.INFO, 'changes have implemented!')
            return redirect('cart:cart_view', username=username)
    else:
        return redirect('cart:cart_view', username=request.user.username)


@login_required
def cart_remove_item(request, username, item_id=None):
    cart = User.objects.get(username=username).profile.profile_cart
    del cart.items[item_id]
    cart.save()
    return redirect('cart:cart_view', username=username)


@login_required
def cart_clean(request, username):
    cart = User.objects.get(username=username).profile.profile_cart
    cart.items = {}
    cart.save()
    return redirect('cart:cart_view', username=username)


@login_required
@csrf_exempt
def cart_discount_coupon(request):
    if request.is_ajax and request.method == 'GET':
        print('ok')
        print(request.GET['coupon_code'])
    else:
        print('holl')
