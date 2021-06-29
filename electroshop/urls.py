from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from filebrowser.sites import site

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from profile import serializers as profile_serializer
from cart import serializers as cart_serializer

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-users/', include(profile_serializer.router.urls)),
    path('api-carts/', include(cart_serializer.router.urls)),
    # path('api/', include('salesman.urls')),
    path('social-login/', include('social_login.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('order.urls')),
    path('profile/', include('profile.urls')),
    path('checkout/', include('checkout.urls')),
    path('wagtail/', include(wagtail_urls)),
    path('tinymce/', include('tinymce.urls')),
    path('django-admin/filebrowser/', site.urls),
    path('', include('shop.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
