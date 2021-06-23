from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profile.models import Profile
from cart.models import Cart
from order.models import Order
import requests
import json


@login_required
def checkout(request, username):
    profile = Profile.objects.get(user=User.objects.get(username=username))
    cart = profile.profile_cart
    context = {'profile': profile, 'cart': cart}
    return render(request, 'checkout_checkout.html', context)


"""
آقای پرداخت

def pay(request, username):
    profile = User.objects.get(username=username).profile
    cart = profile.profile_cart

    api_key = 'aqayepardakht'
    callback_url = 'http://127.0.0.1:8000/'
    url1 = 'https://panel.aqayepardakht.ir/api/create'
    data = {'pin': api_key, 'amount': cart.total_price, 'callback': callback_url,
            'mobile': profile.phone, 'description': 'خرید از فروشگاه الکتروشاپ'}

    r = requests.post(url=url1, data=data)
    print(r.status_code)
    if r.status_code == 200 and not r.text.replace('-', '').isdigit():
        transaction_id = r.text
        print(f'transaction_id: {transaction_id}')
        return redirect(f'https://panel.aqayepardakht.ir/startpay/{transaction_id}')
    else:
        message = f'Error has occurred! error code:\n {r.text}'
        return HttpResponse(f'<h1>{message}</h1>')

"""


def pay(request, username):
    profile = User.objects.get(username=username).profile
    cart = profile.profile_cart
    callback = f'http://127.0.0.1:8000/checkout/{username}/payment/'
    url = 'https://api.idpay.ir/v1.1/payment'
    headers = {'Content-Type': 'application/json', 'X-API-KEY': '6a7f99eb-7c20-4412-a972-6dfb7cd253a4',
               'X-SANDBOX': '1'}
    data = {'order_id': 100, 'amount': cart.total_price * 10, 'name': profile.user.username,
            'phone': profile.phone, 'mail': profile.user.email, 'desc': 'خرید از الکتروشاپ',
            'callback': callback}
    r = requests.post(url=url, json=data, headers=headers)
    print(r.status_code)
    print(r.json())
    Order.objects.create(profile=profile, order_id=r.json()['id'])
    cart.order_id = r.json()['id']
    cart.save()
    return redirect(to=r.json()['link'])


@csrf_exempt
def verify(request, username):
    user = User.objects.get(username=username)
    cart = Cart.objects.get(profile=user.profile)
    order = Order.objects.get(order_id=cart.order_id)
    headers = {'Content-Type': 'application/json', 'X-API-KEY': '6a7f99eb-7c20-4412-a972-6dfb7cd253a4',
               'X-SANDBOX': '1'}
    data = {'id': order.order_id, 'order_id': 100}
    r = requests.post(url='https://api.idpay.ir/v1.1/payment/verify', headers=headers, data=json.dumps(data))
    print(r.status_code)
    print(r.json())
    if r.status_code == 200:
        order.is_Paid = True
        order.save()
        cart.items = {}
        cart.save()
        return redirect(to='checkout:success_pay', username=username)
    return HttpResponse('پرداخت موفقیت آمیز نبود')


def success_pay(request, username):
    profile = User.objects.get(username=username).profile
    order = profile.profile_orders.last()
    context = {'profile': profile, 'order': order}
    return render(request, 'checkout_success_pay.html', context)
