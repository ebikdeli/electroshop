from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
# from electroshop.settings import dev


def discount_model_validator(discount: float) -> float:  # validate 'discount_percent' field before saved into database
    if discount < 0.0:
        raise ValidationError('percent is less than zero')
    if discount > 100.0:
        raise ValidationError('percent is too high')
    if 1.0 <= discount <= 100.0:
        return discount / 100
    if 0.0 <= discount < 1.0:
        return discount


def customer_directory_path(instance, filename):    # To save users' logo in custom path
    if not instance.user.email:
        return f'customer_{instance.user.username}/{filename}'
    return f'{instance.user.email}/{filename}'


class Profile(models.Model):
    # user = models.OneToOneField(dev.AUTH_USER_MODEL,
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True)
    address = models.TextField(blank=True)
    score = models.PositiveIntegerField(default=0)
    discount_value = models.PositiveIntegerField(default=0)
    discount_percent = models.FloatField(validators=[MaxValueValidator(100),
                                                     MinValueValidator(0),
                                                     discount_model_validator],
                                         default=0)
    lifetime_orders_price = models.PositiveIntegerField(default=0)
    picture = models.ImageField(upload_to=customer_directory_path, blank=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # likes

    class Meta:
        ordering = ['updated']

    def __str__(self):
        # return self.user.username + '_profile'
        return f'{self.user.username}_profile'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        self.discount_percent = discount_model_validator(self.discount_percent)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('someview', args=[str(self.id), self.slug])
