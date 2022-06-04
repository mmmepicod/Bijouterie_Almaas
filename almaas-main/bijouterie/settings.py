from pathlib import Path

import os
import environ

# Construire route sur une base: BASE_DIR / 'sous directio'.
BASE_DIR = Path(__file__).resolve().parent.parent


env=environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)

if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))

# clef securite en mode production
SECRET_KEY = "django-insecure-3%y3laftm62q0zaj+s7#p-xqq9(&#q+)s8)p-&#&bz*0$!xu$0"

# mod debug true, mettre à false en mode production
DEBUG = env.bool("DEBUG", default=True)

# DEBUG = False

ALLOWED_HOSTS = ['*']


# applications installées, rajouter celles qu'on construit aux natives, ici notre appli "store"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    'crispy_forms',
    'django_htmx',
    'whitenoise.runserver_nostatic',

    "store",



]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "bijouterie.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_preprocessors.store_menu",
                "store.context_preprocessors.cart_menu",
            ],
        },
    },
]

WSGI_APPLICATION = "bijouterie.wsgi.application"


# BDD mode fichier :
# Base sqlite3

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "magasin.sqlite3",
    }
}


# BDD mode serveur:
# Base MariaDB

#DATABASES = {
#   'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'siteenconstruction_ptut',
#        'HOST': 'mysql-siteenconstruction.alwaysdata.net',
#        'PORT': '3306',
#        'USER': '267284',
#        'PASSWORD': 'apprendre',
#    }
#}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# paramètres d'internationalisation


LANGUAGE_CODE = "en-US"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# réglages paramètres static


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "bijouterie/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # Automatically Created on Production

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# réglages Media ( change l'endroit et la façon dont django stoque les fichiers
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Type de champ clé primaire à utiliser par défaut pour les modèles n’ayant pas de champ avec primary_key=True.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


#ici j'ai mis mon id PAYPAL
CLIENT_ID = "AU5cjgYiAgdV69njj9Y8RdSLHOWDs6nekyalUZdFqYkq1gXdJnpqhNLO4nHy81VYdacx24XYLBKeJuCJ"

CRISPY_TEMPLATE_PACK = 'bootstrap4'