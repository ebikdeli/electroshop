from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profile.models import Profile
from cart.models import Cart
from order.models import Order
from sendmail.tasks import send_checkout_mail
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


@login_required
def pay(request, username):
    profile = User.objects.get(username=username).profile
    cart = profile.profile_cart
    callback = f'http://127.0.0.1:8000/checkout/{username}/payment/'
    url = 'https://api.idpay.ir/v1.1/payment'
    headers = {'Content-Type': 'application/json', 'X-API-KEY': '6a7f99eb-7c20-4412-a972-6dfb7cd253a4',
               'X-SANDBOX': '1'}
    data = {'order_id': 100, 'amount': cart.price_after_discount * 10, 'name': profile.user.username,
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
@login_required
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
        cart.items = dict()
        cart.save()
        return redirect(to='checkout:success_pay', username=username)
    return HttpResponse('پرداخت موفقیت آمیز نبود')


@login_required
def success_pay(request, username):
    profile = User.objects.get(username=username).profile
    order = profile.profile_orders.last()
    html_message = f'Dear customer <strong>{profile.user.username}</strong>, this is your checkout. Save this email!<br>' \
                   f'<strong>Order id: {order.order_id}</strong><br><strong>Price: {order.total_price}</strong> toman<br>' \
                   f'<strong>Total Items: {order.total_items}</strong> adad<br>' \
                   f'<bold>Items:</bold><br>'
    for item_id, numbers in order.items.items():
        for item in order.products.all():
            if item_id == item.product_id:
                html_message += f'{item.brand.name} {item.name}: {numbers} addad ' \
                                f'{item.price * numbers} tomans'
    html_message += '<h2>بابت اعتماد به ما از شما متشکریم</h2>'
    result = send_checkout_mail.delay(subject='ارسال فاکتور',
                                      message='این فاکتور به منزله پرداخت موفقیت آمیز است.',
                                      from_email=settings.EMAIL_HOST_USER,
                                      recipients=[profile.user.email, 'arash.pouya.c@gmail.com'],
                                      html_message=html_message,
                                      )
    if result == 1:
        print('email sent!')
    context = {'profile': profile, 'order': order}
    return render(request, 'checkout_success_pay.html', context)
