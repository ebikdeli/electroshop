from django.db import models
from profile.models import Profile
from cart.models import Cart
from shop.models import Product


class Order(models.Model):
    profile = models.ForeignKey(to=Profile,
                                related_name='profile_orders',
                                on_delete=models.CASCADE)
    products = models.ManyToManyField(to=Product,
                                      related_name='product_orders',
                                      blank=True)
    items = models.JSONField(default=dict)
    order_id = models.CharField(max_length=30)
    total_price = models.PositiveIntegerField(default=0)
    total_items = models.PositiveIntegerField(default=0)
    is_Paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f'{self.profile.user.username}_{self.order_date}_order_id: {self.order_id}'

    def save(self, *args, **kwargs):
        if self.is_Paid:
            cart = self.profile.profile_cart
            self.items = cart.items
            self.total_price = cart.total_price
            self.total_items = cart.total_number
            for product in cart.product.all():
                self.products.add(product)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
