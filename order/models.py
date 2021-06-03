from django.db import models
from profiles.models import Profile
from cart.models import Cart


class Order(models.Model):
    profile = models.ForeignKey(to=Profile,
                                related_name='profile_orders',
                                on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart,
                             on_delete=models.CASCADE,
                             related_name='order_cart')
    order_id = models.CharField(max_length=30)
    order_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'order_number: ' + self.order_id
