"""
Django settings for omniartiste project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4e-*f2yz&c8b-dbw+h4&a+%widv4%*tim89$z&w^qig%s!gf()'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'pages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'omniartiste.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'omniartiste.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'omniartiste',                      
        'USER': 'postgres',
        'PASSWORD': 'aayush',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'  # URL to access static files

# Define the path where static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directories where Django will look for static files in the project
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'support@omniartiste.org'  # Replace with your Namecheap Private Email address
EMAIL_HOST_PASSWORD = 'OmniBrian@123'      # Replace with your Namecheap Private Email password
DEFAULT_FROM_EMAIL = 'support@omniartiste.org'  # Replace with your Namecheap Private Email address
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STRIPE_SECRET_KEY = 'sk_test_51MsYaVIj9JFN5Py8IXRrKU4m54jcVcdYpOaOMue8vIViYaLgyu9lQmmpBERJ0kgLjcSiUdkb4iMx7FFKaLiHAGyt00RFmLkIEf'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51MsYaVIj9JFN5Py8ttbhr1SvNPFQxIJs31AjnD7QJmbc0FbAahnkSjlvIENI4BSZJ4JRNBoBYdg0FeaGHeBN5ugG00NQfe7HzC'