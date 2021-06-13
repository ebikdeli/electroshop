from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
    path('api/', include('salesman.urls')),
    path('social-login/', include('social_login.urls')),
    path('cart/', include('cart.urls')),
    path('profile/', include('profile.urls')),
    # path('order/', include('order.urls')),
    path('wagtail/', include(wagtail_urls)),
    path('', include('shop.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
