from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register,\
                                                ModelAdminGroup

from mainshop.models import Category, Brand, Product


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = 'Category'
    menu_order = 200


class BrandAdmin(ModelAdmin):
    model = Brand
    menu_label = 'Brand'
    menu_order = 200


class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = 'Product'
    menu_order = 200


"""
modeladmin_register(CategoryAdmin)
modeladmin_register(BrandAdmin)
modeladmin_register(ProductAdmin)
"""


class ShopManagerAdmin(ModelAdminGroup):
    menu_label = 'ShopManager'
    menu_order = 200
    items = [CategoryAdmin, BrandAdmin, ProductAdmin]


modeladmin_register(ShopManagerAdmin)
