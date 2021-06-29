from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from profile.models import Profile
from shop.models import Category, Brand, Product
from shop.forms import ProductQuantity


def index(request):
    try:
        categories = Category.objects.all()
    except Category.DoesNotExist:
        categories = None

    try:
        request.user.profile

    except Profile.DoesNotExist:
        return redirect('profile:edit_profile', username=request.user.username)
    except AttributeError:
        pass

    return render(request, 'index.html', {'categories': categories})


class ProductView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    queryset = Product.objects.all()
    template_name = 'shop_product_list.html'


def product_detail(request, product_id=None):
    if request.method == 'POST':
        product_quantity_form = ProductQuantity(data=request.POST)
        if product_quantity_form.is_valid():
            product_quantity = product_quantity_form.cleaned_data['quantity']
            cart = request.user.profile.profile_cart
            cart.items[str(product_id)] = product_quantity
            cart.save()
            return redirect('cart:cart_view', username=request.user.username)

    else:
        product_quantity_form = ProductQuantity(initial={'quantity': 1})

    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        print('Product does not exist!')
        return redirect('shop:product_list')

    return render(request, 'shop_product_detail.html', {'product': product,
                                                        'product_quantity_form': product_quantity_form})
