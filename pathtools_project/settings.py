"""
Django settings for pathtools_project project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

### PROD SETTINGS ###

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT  = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#STATICFILES_DIRS = [STATIC_DIR, ]   

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

MEDIA_ROOT = MEDIA_DIR

MEDIA_URL = '/media/'

APPEND_SLASH = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

ALLOWED_HOSTS = ['127.0.0.1', '10.88.45.54', 'pathtools.ccf.org']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dx_search',
    'registration',
    'django_password_validators',
    'django_password_validators.password_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [

        'django.contrib.auth.backends.ModelBackend',
        ]


ROOT_URLCONF = 'pathtools_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pathtools_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'my_cache_table',
            }
        }


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
    {
        'NAME': 'django_password_validators.password_history.password_validation.UniquePasswordsValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumberValidator'
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

SITE_NAME = 'Pathtools' 

DEFAULT_FROM_EMAIL = 'noreply@pathtools.ccf.org'

ADMINS = [('Scott', 'roberts10@ccf.org'),] 


REGISTRATION_OPEN = True 

ACCOUNT_ACTIVATION_DAYS = 7

#REGISTRATION_AUTO_LOGIN = 

#EXPIRED_REDIRECT_URL = '/pathtools_dev/dx_search/password/change_expired'
#EXPIRED_REDIRECT_URL = '/pathtools/dx_search/password/change_expired'
EXPIRED_REDIRECT_URL = '/dx_search/password/change_expired'

#LOGIN_REDIRECT_URL = '/pathtools_dev/dx_search'
#LOGIN_REDIRECT_URL = '/pathtools/dx_search'
LOGIN_REDIRECT_URL = '/dx_search'

#LOGIN_URL = 'pathtools_dev/dx_search/login'
#LOGIN_URL = 'pathtools/dx_search/login'
LOGIN_URL = '/dx_search/login'

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 30 

SECURE_SSL_REDIRECT = True

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'default',
                #'filename': '/home/robertsons/www/DEV_pathtools/pathtools/debug.log',
                'filename': '/home/robertsons/www/pathtools/debug.log',
                },
            'file_info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'formatter': 'default',
                #'filename': '/home/robertsons/www/DEV_pathtools/pathtools/info.log',
                'filename': '/home/robertsons/www/pathtools/info.log',
                },
            },
        'formatters': {
            'default': {
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
                    }
            },
        'loggers': {
            # 'django': {
            #     'handlers': ['file'],
            #     'level': 'INFO',
            #     'propagate': True,
            #     },
            'dx_search.views': {
                'handlers': ['file', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'dx_search.forms': {
                'handlers': ['file', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
                },
            },
        }