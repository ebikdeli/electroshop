from django.test import TestCase
from django.contrib.auth.models import User
from profile.models import Profile
from shop.models import Category, Brand, Product
from cart.models import Cart


class CartTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='ehsan')
        Profile.objects.create(user=user, phone='09376736885')
        c1 = Category.objects.create(name='tablet')
        c2 = Category.objects.create(name='laptop')
        c3 = Category.objects.create(name='smartphone')
        b1 = Brand.objects.create(name='samsung', founded='1950')
        b2 = Brand.objects.create(name='apple', founded='1975')
        b3 = Brand.objects.create(name='hp', founded='1945')
        p1 = Product.objects.create(name='db1100ny', brand=b3, price=500)
        p1.category.add(c1, c2)
        p2 = Product.objects.create(name='galaxy s3', brand=b2, price=1000)
        p2.category.add(c3)

    def test_profile(self):
        profile = Profile.objects.get(phone='09376736885')
        print(profile)
        p1 = Product.objects.get(name='db1100ny')
        print(p1, ' ', p1.product_id, '\n', p1.category.all())
        p2 = Product.objects.get(name='galaxy s3')

        cart = Cart.objects.create(profile=profile, items={p1.product_id: 3, p2.product_id: 2})
        print(cart, 'total_number=', cart.total_number, ' total_price=', cart.total_price,'\n', cart.product.all())

