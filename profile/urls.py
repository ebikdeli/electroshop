from django.urls import path
from profile import views


app_name = 'profile'

urlpatterns = [
    path('profile_login/', views.profile_login, name='profile_login'),
    path('user/login_signup/', views.user_login_signup, name='login_signup'),
    path('user/sigup/', views.user_signup, name='user_signup'),
    path('user/login/', views.user_login, name='user_login'),
    path('<username>/', views.profile_view, name='profile_view'),
    path('<username>/edit/', views.profile_edit, name='edit_profile'),
    path('<username>/logout/', views.user_logout, name='user_logout')
]
