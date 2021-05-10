from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from taggit.managers import TaggableManager

app_name = 'mainshop'


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    tags = TaggableManager()


class Brand(models.Model):
    name =

class Product(models.Model):
    name = models.CharField(max_length=30)
    pass
