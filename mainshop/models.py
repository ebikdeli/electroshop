from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class Product(Page):
    name = models.TextField(max_length=20)
    description = RichTextField(max_length=250, blank=True)

    content_panels = Page.content_panels + [FieldPanel('description', heading='توصیف محصول'),
                                            FieldPanel('name', 'نام محصول')]
