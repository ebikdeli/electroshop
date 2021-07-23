from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from profile.models import Profile
from cart.models import DiscountCode, discount_hpercent
from cart.forms import ChangeCart, CouponCode


@login_required
def cart_view(request, username):
    # cart = Profile.objects.get(user=User.objects.get(username=username)).profile_cart
    change_cart_form = ChangeCart()
    context = {'change_cart_form': change_cart_form}
    return render(request, 'cart_view.html', context)


@login_required
def cart_change_item(request, username, item_id):
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
        if request.is_ajax() and request.method == 'GET':
            data = request.GET
            print(data)
            cart.items[data['item_id']] = int(data['new_quantity'])
            cart.save()
            return redirect('cart:cart_view', username=username)
        else:
            return redirect('cart:cart_view', username=request.user.username)


@login_required
def cart_remove_item(request, username, item_id):
    print(f'data recieved from ajax: username: {username}, item_id: {item_id}')
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
        recv_data = request.GET
        raw_data = dict(recv_data)
        print(raw_data)
        cuopon_code = request.GET['coupon_code']
        print(cuopon_code)
        try:
            discount_code = DiscountCode.objects.get(code=cuopon_code)
            profile = request.user.profile

            if discount_code.value:
                profile.discount_value += discount_code.value
                profile.save()

            if discount_code.percent:
                discount_percent = discount_hpercent(discount_code.percent)
                profile.discount_percent += discount_percent

                if profile.discount_percent >= 0.5:
                    profile.discount_percent = 0.5
                profile.save()

        except DiscountCode.DoesNotExist:
            print('oh noooooo')
            return JsonResponse({'error': 'کد اشتباه است', 'status': 201}, status=201, safe=False)
        if not discount_code.is_valid:
            return JsonResponse({'error': 'این کد قبلا استفاده شده', 'status': 201}, status=201, safe=False)
        if discount_code.percent:
            pass
        if discount_code.value:
            return JsonResponse({'value': discount_code.value, 'status': 200}, status=200, safe=False)
    else:
        print('holl')
        return JsonResponse({'error': 'خطایی در سمت سرور پیش آمده', 'status': 401}, status=401, safe=False)
