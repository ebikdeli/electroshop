from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('product_list/', views.ProductView.as_view(), name='product_list'),
    path('product/<product_id>/', views.product_detail, name='product_detail'),
]
