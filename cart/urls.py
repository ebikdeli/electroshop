from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('<username>/', views.cart_view, name='cart_view'),
    path('<username>/<item_id>/change/', views.cart_change_item, name='cart_change_item'),
    path('<username>/<item_id>/remove/', views.cart_remove_item, name='cart_remove_item'),
    path('<username>/clean/', views.cart_clean, name='cart_clean'),
    path('coupon/valid/', views.cart_discount_coupon, name='cart_coupon'),
]
