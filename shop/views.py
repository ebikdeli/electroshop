import celery
import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from profile.models import Profile
from shop.models import Category, Brand, Product
from shop.forms import ProductQuantity


def index(request):
    try:
        # product_discounted = Product.objects.all().filter() # filter by 'discounted' field
        product_discounted = Product.objects.all()

        # product_offered = Product.objects.all().filter()  # filter by 'special_offer' field
        product_offered = Product.objects.all()
    except Product.DoesNotExist:
        product_discounted = None
        product_offered = None
    try:
        categories = Category.objects.all()
    except Category.DoesNotExist:
        categories = None

    try:
        request.user.profile

    except Profile.DoesNotExist:
        print('why profile not exist?')
        return redirect('profile:edit_profile', username=request.user.username)
    except AttributeError:
        pass

    product_discounted_counter = 4
    product_special_offer_counter = 4
    return render(request, 'index.html', {'categories': categories,
                                          'product_discounted': product_discounted,
                                          'product_offered': product_offered,
                                          'product_discount_counter': product_discounted_counter,
                                          'product_special_offer_counter': product_special_offer_counter})


"""
def products_in_category(request, slug=None):
    categories = Category.objects.all()
    product = Product.objects.get(category=Category.objects.get(slug=slug))
    return render(request, 'shop_category.html', context={'categories': categories,
                                                          'product': product})
"""


class CategoryView(DetailView):
    model = Category
    paginate_by = 12
    context_object_name = 'category'
    template_name = 'shop_category.html'
    category_name = None

    def get(self, request, slug=None, *args, **kwargs):
        self.category_name = Category.objects.get(slug=slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all().filter(category=Category.objects.get(name=self.category_name))
        return context


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
