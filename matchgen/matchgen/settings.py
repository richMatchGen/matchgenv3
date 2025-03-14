"""
Django settings for matchgen project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Media files (for generated images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (for pre-designed templates)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]



load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l$+vq*7%9#i&--f_&aio*h3qo6encuxgytx9pgs1v2+6743u!_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',  # Admin panel
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',  # Ensure the users app is registered
    'social_django',  # Django Social Auth
]

# Set session expiration time (e.g., 30 minutes)
SESSION_COOKIE_AGE = 30 * 60  # 30 minutes in seconds

# Make session expire when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTHENTICATION_BACKENDS = [
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
# TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
# TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")


SOCIAL_AUTH_FACEBOOK_KEY = "YOUR_FACEBOOK_APP_ID"
SOCIAL_AUTH_FACEBOOK_SECRET = "YOUR_FACEBOOK_APP_SECRET"

SOCIAL_AUTH_INSTAGRAM_KEY = "YOUR_INSTAGRAM_APP_ID"
SOCIAL_AUTH_INSTAGRAM_SECRET = "YOUR_INSTAGRAM_APP_SECRET"

# Allow storing OAuth tokens securely
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = True

# URL to redirect users after authentication
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Allow frontend requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # ✅ React Frontend URL
]

CORS_ALLOW_CREDENTIALS = True  # ✅ MUST be True to allow cookies & authentication

ROOT_URLCONF = 'matchgen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'matchgen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'matchgen_db',
        'USER': 'matchgen_user',
        'PASSWORD': '@Vale1923',
        'HOST': 'localhost',
        'PORT': '5432',
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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
