from django.db import models

from wagtail.core.fields import RichTextField

from django_countries.fields import CountryField
from taggit.managers import TaggableManager

from datetime import datetime
import uuid


def founded_choice():
    min_year = 1900
    max_year = datetime.now().year
    year_list = [('< '+str(min_year), '< '+str(min_year))]
    for year in range(min_year, max_year+1):
        year_list.append((str(year), str(year)))
    return year_list


class Category(models.Model):
    name = models.CharField(max_length=30)
    tags = TaggableManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30)
    country = CountryField(blank=True)
    founded = models.CharField(max_length=6, blank=True, choices=founded_choice())
    founder = models.CharField(max_length=10, blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.CharField(default=uuid.uuid4, max_length=36)
    name = models.CharField(max_length=30)
    category = models.ManyToManyField(to=Category,
                                      related_name='product_category')
    brand = models.ForeignKey(to=Brand,
                              related_name='Product_brand',
                              on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    in_stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    description = RichTextField(blank=True)
    review = RichTextField(blank=True)

    class Meta:
        ordering = ['name', 'available']

    def __str__(self):
        return self.name
