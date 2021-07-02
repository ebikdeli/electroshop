from django.urls import path
from profile import views


app_name = 'profile'

urlpatterns = [
    path('profile_login/', views.profile_login, name='profile_login'),
    path('login_signup/', views.user_login_signup, name='login_signup'),
    path('<username>/edit/', views.profile_edit, name='edit_profile'),
]
