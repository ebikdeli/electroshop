from django.db import models
from profile.models import Profile
from shop.models import Product


class Cart(models.Model):
    profile = models.OneToOneField(to=Profile,
                                   related_name='profile_cart',
                                   on_delete=models.CASCADE)
    product = models.ManyToManyField(to=Product,
                                     related_name='product_cart',
                                     blank=True)
    items = models.JSONField(blank=True, default=dict)  # per documents
    total_price = models.PositiveIntegerField(default=0)
    total_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.profile.user.username + '_cart'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        total_price = 0
        total_number = 0
        product_list = []

        if self.items:
            for product_id, number in self.items.items():
                product_list.append(Product.objects.get(product_id=product_id))
                total_price += product_list[-1].price * number
                total_number += number

            [self.product.add(prod) for prod in product_list]
            self.total_price = total_price
            self.total_number = total_number
        else:
            self.product.set('')
            self.total_number = 0
            self.total_price = 0
        super().save(*args, **kwargs)
