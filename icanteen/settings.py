"""
Django settings for icanteen project.

Generated by 'django-admin startproject' using Django 1.11b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4jp(lm_@kl5w86$wjb9nke8i@^$w6artpq8u&ce3s7u9(u44nq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '*']


# Application definition

INSTALLED_APPS = [
    'users',
    'maps',
    'polls',
    'payments',
    'home',
    'slideshow',
    'gallery',
    'cart',
    'orders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'crispy_forms',
    'crispy_bootstrap4',
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'icanteen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'icanteen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
LOGIN_REDIRECT_URL = "users:dashboard"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CART_SESSION_ID = 'cart'
# this is the key going to be used to the cart during user sessions

#For email

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'tamunang.courage@ictuniversity.org'
# EMAIL_HOST_PASSWORD = 'utykydfqeenxvxgg'
# EMAIL_PORT = 587
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sas.bergson@gmail.com'
DEFAULT_FROM_EMAIL = 'sas.bergson@gmail.com'
EMAIL_HOST_PASSWORD = 'yfmhdehvhuseicca'

#This did the trick

# A logger is the entry point into the logging system. Each logger is a named bucket to 
# which messages can be written for processing.
# A logger is configured to have a log level. This log level describes the severity of 
# the messages that the logger will handle. Python defines the following log levels:

# DEBUG: Low level system information for debugging purposes
# INFO: General system information
# WARNING: Information describing a minor problem that has occurred.
# ERROR: Information describing a major problem that has occurred.
# CRITICAL: Information describing a critical problem that has occurred.

# Each message that is written to the logger is a Log Record. 
# Each log record also has a log level indicating the severity of that specific message. 
# A log record can also contain useful metadata that describes the event that is being logged. 
# This can include details such as a stack trace or an error code.


# LOGGING = {
#     'version': 1,
#      # The version number of our log
#     'disable_existing_loggers': False,
#     # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
#     # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
#     'formatters': {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     # "filters": {
#     #     "require_debug_true": {
#     #         "()": "django.utils.log.RequireDebugTrue",
#     #     },
#     # },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'email': {
#             'level': 'DEBUG',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'include_html': True,
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#             'formatter': 'verbose',
#         },
#     },
#     # Define the root logger's settings
#     'root': {
#         'handlers': ['console'],
#         'level': 'DEBUG',
#     },
#     # Define the django log module's settings
#     'loggers': {
#         'django': {
#             'handlers': ['console','file'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#             "propagate": True,
#         },
#         'users': {
#             'handlers': ['console','email','file'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#             "propagate": True,
#         },
#     },
# }

# INTERNAL_IPS = [
#     'localhost', 
#     '127.0.0.1', 
#     '[::1]', 
#     '*'
# ]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

