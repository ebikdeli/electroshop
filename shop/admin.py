from django.contrib import admin
from shop.models import Category, Brand, Product,\
    ProductImages, Camera


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Camera)


class CameraInlineAdmin(admin.TabularInline):
    model = Camera


class ProductImageInlineAdmin(admin.StackedInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [CameraInlineAdmin, ProductImageInlineAdmin]
