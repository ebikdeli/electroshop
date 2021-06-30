from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation

from wagtail.core.fields import RichTextField

from profile.models import discount_model_validator
from user_activity.models import Comment

from django_countries.fields import CountryField
from taggit.managers import TaggableManager

from datetime import datetime
import uuid
import os

# CATEGORY_DEFAULT_BACKGROUND = os.path.join(settings.BASE_DIR, 'shop', 'static', 'images', 'mainboard.jpg')


def founded_choice():
    min_year = 1900
    max_year = datetime.now().year
    year_list = [('< '+str(min_year), '< '+str(min_year))]
    for year in range(min_year, max_year+1):
        year_list.append((str(year), str(year)))
    return year_list


def category_directory_path(instance, filename):
    return f'category_{instance.name}_bg/{filename}'


def brand_directory_path(instance, filename):
    return f'logo_{instance.name}/{filename}'


def product_directory_path(instance, filename):    # To save product logo in custom path
    return f'{instance.brand.name}_{instance.name}_{instance.id}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=30)
    name_persian = models.CharField(max_length=30, blank=True)
    background_image = models.ImageField(upload_to=category_directory_path,
                                         default='category_default.jpg')
    tags = TaggableManager(blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=30)
    country = CountryField(blank=True)
    logo = models.ImageField(upload_to=brand_directory_path,
                             blank=True)
    founded = models.CharField(max_length=6, blank=True, choices=founded_choice())
    founder = models.CharField(max_length=10, blank=True)
    tags = TaggableManager(blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
    discount_value = models.PositiveIntegerField(default=0)
    discount_percent = models.FloatField(validators=[MaxValueValidator(100),
                                                     MinValueValidator(0),
                                                     discount_model_validator],
                                         default=0)
    special_offer = models.BooleanField(default=False)
    picture = models.ImageField(blank=True, upload_to=product_directory_path)
    description = RichTextField(blank=True)
    review = RichTextField(blank=True)
    tag = TaggableManager(blank=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    comment = GenericRelation(Comment)

    class Meta:
        ordering = ['name', 'available']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand.name}_{self.name}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'product_id': self.product_id})


class ProductImages(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='product_images')
    image = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.brand.name}_{self.product.name}_image{self.id}'
