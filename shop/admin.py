from django.contrib import admin
from shop.models import Category, Brand, Product,\
    ProductImages


admin.site.register(Category)
admin.site.register(Brand)


class ProductImageInlineAdmin(admin.StackedInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInlineAdmin]
