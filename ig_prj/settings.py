"""
Django settings for ig_prj project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

load_dotenv()

# Retrieve secret keys
CONTENT_ANALYSIS_API_KEY = os.getenv("CONTENT_ANALYSIS_API_KEY")
CONTENT_ANALYSIS_API_SECRET = os.getenv("CONTENT_ANALYSIS_API_SECRET")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k1l8gsqp&&glb@%qafi26xb-y4%xjf60g)2!6bspqc+@xjl7me'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    #own
    'post',
    'crispy_forms',
    'authy',
    'comment',
    'directs',
    'notification',
    'reels',
    'custom_admin',
    'crispy_bootstrap4',
    'rest_framework',
    'corsheaders',
    'chatbot',
    'stories',
    # 'content_analyzer',
    'password',
    'marketplace',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ig_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ig_prj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'sign-in'

LOGIN_URL = 'sign-in'

CRISPY_TEMPLATE_PACK = 'bootstrap4'


JAZZMIN_SETTINGS = {
    # Basic setup
    "site_title": "Instagram Clone Admin",
    "site_header": "Instagram Clone Dashboard",
    "site_brand": "InstaClone",
    "welcome_sign": "Welcome to InstaClone Admin Panel",
    "copyright": "InstaClone © 2025",
    "user_avatar": "profile.picture",  # Assuming your `Profile` model has a `picture` field

    # Logo and branding
    "site_logo": "C:/Users/roicy/Downloads/Instagram-Clone/static/assets2/images/logo.png",  # Add your logo here (place it in the static folder)
    "site_icon": "your_app_name/images/favicon.ico",  # Add a favicon (optional)
    "login_logo": "your_app_name/images/login_logo.png",  # Custom login page logo
    "login_logo_dark": True,  # Optional dark-mode logo
    "show_sidebar": True,
    "navigation_expanded": False,  # Keep the navigation collapsed by default
    "hide_apps": ["auth"],  # Optional: Hide irrelevant apps like `auth`
    "hide_models": ["auth.Group"],  # Optional: Hide unnecessary models
    "order_with_respect_to": ["auth", "comment", "profile"],

    # UI Tweaks
    "changeform_format": "single",  # Make form fields look more compact
    "changeform_format_overrides": {
        "auth.user": "collapsible",  # Specific formatting for auth users
    },
    "language_chooser": True,

    # Custom Links
    "custom_links": {
        "profile": [
            {
                "name": "View Profile Stats",
                "url": "https://your-website.com/admin/profile/",
                "icon": "fas fa-chart-bar",
                "permissions": ["profile.view_profile"],
            }
        ],
    },

    # Icons for apps and models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "comment.Comment": "fas fa-comments",
        "post.Post": "fas fa-image",
        "profile.Profile": "fas fa-user-circle",
        "stream.Stream": "fas fa-video",
        "reel.Reel": "fas fa-film",
        "follow.Follow": "fas fa-user-plus",
    },

    # Top Menu Links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
        {
            "model": "profile.profile",
        },
        {
            "name": "Support",
            "url": "https://your-support-url.com",
            "new_window": True,
        },
    ],

    # Sidebar Links
    "usermenu_links": [
        {"name": "Support", "url": "https://your-support-url.com", "new_window": True},
        {"model": "auth.user"},
    ],

    # Theme Customization
    "theme": "cerulean",  # Themes: 'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', etc.
    "dark_mode_theme": "cyborg",  # Optional dark mode

    # Analytics (Optional)
    "show_google_analytics": True,
    "google_analytics": "UA-XXXXX-Y",  # Replace with your Google Analytics tracking code
}

LANGUAGE_CODE = "en"  # Default language

# Add the languages you want to support
LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    # Add more languages as needed
]

# Optional: Configure translation files
LOCALE_PATHS = [
    BASE_DIR / "locale",  # Path where your translation files are stored
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '041129roycy@gmail.com'
EMAIL_HOST_PASSWORD = 'gmfq spqf ejcs rdix'