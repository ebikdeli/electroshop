from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from taggit.managers import TaggableManager
from django_countries.fields import CountryField

app_name = 'mainshop'


class Category(models.Model):
    name = models.CharField(max_length=20)
    tags = TaggableManager()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30)
    country = CountryField(blank=True)
    founded = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30,
                            )
    category = models.ForeignKey(Category,
                                 related_name='product_category',
                                 on_delete=models.CASCADE,
                                 )
    brand = models.ForeignKey(Brand,
                              related_name='product_brand',
                              on_delete=models.CASCADE,
                              )
    model = models.CharField(max_length=4, blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.brand.name + ' ' + self.name
