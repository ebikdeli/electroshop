from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!#$0r-b62#54z7i^0p-_)_&h8kl6c&ec8yo(95sz$!##l9qrsf'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
