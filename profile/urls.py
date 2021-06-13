from django.urls import path
from profile import views


app_name = 'profile'

urlpatterns = [
    path('profile_login/', views.profile_login, name='profile_login'),
    path('profile_create/', views.profile_create, name='create_user'),
    path('<username>/edit/', views.profile_edit, name='edit_profile'),
]
