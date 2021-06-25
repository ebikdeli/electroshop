from django.urls import path
from checkout import views

app_name = 'checkout'

urlpatterns = [
    path('<username>/', views.checkout, name='checkout'),
    path('<username>/pay/', views.pay, name='pay'),
    path('<username>/payment/', views.verify, name='pgi'),
    path('<username>/success_pay/', views.success_pay, name='success_pay')
]
