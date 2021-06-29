from django.db import models
from profile.models import Profile
from shop.models import Product


def discount_hpercent(value: float) -> float:
    if value >= 1.0:
        return value / 100
    return value


class Cart(models.Model):
    profile = models.OneToOneField(to=Profile,
                                   related_name='profile_cart',
                                   on_delete=models.CASCADE)
    product = models.ManyToManyField(to=Product,
                                     related_name='product_cart',
                                     blank=True)
    items = models.JSONField(blank=True, default=dict)  # per documents
    total_price = models.PositiveIntegerField(default=0)
    price_after_discount = models.PositiveIntegerField(default=0)
    total_number = models.PositiveIntegerField(default=0)
    order_id = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.profile.user.username + '_cart'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        total_price = 0
        total_number = 0
        total_discount = 0
        product_list = []

        if self.items:
            for product_id, number in self.items.items():
                product_list.append(Product.objects.get(product_id=product_id))
                total_price += product_list[-1].price * number
                total_number += number

                # 'total_discount' calculates discount only for one item for each product type in the cart
                if product_list[-1].discount_percent or product_list[-1].discount_value:
                    product_list[-1].discount_percent = discount_hpercent(product_list[-1].discount_percent)
                    total_discount += product_list[-1].discount_value + (
                            product_list[-1].price * product_list[-1].discount_percent)

            [self.product.add(prod) for prod in product_list]
            self.total_price = total_price
            self.total_number = total_number
            if self.profile.discount_percent or self.profile.discount_value:
                total_discount += self.profile.discount_value + (
                    self.total_price * self.profile.discount_percent)

            self.price_after_discount = total_price - total_discount
        else:
            self.product.set([])
            self.total_number = 0
            self.total_price = 0
            self.price_after_discount = 0
        super().save(*args, **kwargs)
