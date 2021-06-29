from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('<username>/', views.orders_all, name='all_orders'),
]
