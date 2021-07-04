import os
from django.urls import reverse_lazy


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'tinymce',
    'django_quill',
    "grappelli",
    "filebrowser",

    'home',
    'search',
    'profile',
    'shop',
    'order',
    'checkout',
    'payment',
    'sendmail',
    'cart',
    'social_login',
    'user_activity',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',

    'modelcluster',
    'taggit',

    'salesman.core',
    'salesman.basket',
    'salesman.checkout',
    'salesman.orders',
    'salesman.admin',

    'rest_framework',
    'django_countries',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'electroshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR),
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'shop', 'templates'),
            os.path.join(BASE_DIR, 'cart', 'templates'),
            os.path.join(BASE_DIR, 'profile', 'templates'),
            os.path.join(BASE_DIR, 'checkout', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'cart.context_processor.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'electroshop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR),
    os.path.join(BASE_DIR, 'shop', 'static'),
    os.path.join(BASE_DIR, 'cart'),
    os.path.join(BASE_DIR, 'checkout'),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR)
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TAGGIT_CASE_INSENSITIVE = True

# Authentication settings

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.open_id.OpenIdAuth',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'auth.User'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SITE_ID = 2

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '501246578971-ek7sfvok7qeirn1og4lnoufgobgasvn9.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'tgv7HrR7TPBkNDFnjFrAh90u'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = reverse_lazy('shop:index')
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = reverse_lazy('shop:index')

# Email settings

EMAIL_YAHOO_HOST = 'smtp.mail.yahoo.com'
EMAIL_YAHOO_PASSWORD = 'yizfphuxdgurprwj'
EMAIL_GMAIL_HOST = 'smtp.gmail.com'
EMAIL_GMAIL_PASSWORD1 = 'edxxyxtxztagousa'
EMAIL_GMAIL_PASSWORD2 = 'lcvnujlaamtwcest'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = EMAIL_GMAIL_HOST
EMAIL_HOST_USER = 'ebikdeli@gmail.com'
EMAIL_HOST_PASSWORD = EMAIL_GMAIL_PASSWORD1    # past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'ebikdeli@gmail.com'

# Wagtail settings

WAGTAIL_SITE_NAME = "electroshop"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

# Restful_api
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
