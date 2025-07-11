"""
Impostazioni Django per il progetto Agora_Cultura.

Generato da 'django-admin startproject' usando Django 5.2.1.

Per maggiori informazioni su questo file, vedere
https://docs.djangoproject.com/en/5.2/topics/settings/

Per l'elenco completo delle impostazioni e dei loro valori, vedere
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os

# Costruisci i percorsi all'interno del progetto così: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Impostazioni di sviluppo rapido - non adatte per la produzione
# Vedere https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# AVVISO DI SICUREZZA: mantieni segreta la chiave segreta usata in produzione!
SECRET_KEY = 'django-insecure-s(3)v8)ioj3*8&56r53s^22m*f(_c1k#o66u8liyy#$4h3q0pc'

# AVVISO DI SICUREZZA: non eseguire con debug attivato in produzione!
DEBUG = True

ALLOWED_HOSTS = []


# Definizione delle applicazioni

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AgoraCultura.apps.AgoraculturaConfig',
]

AUTH_USER_MODEL = 'AgoraCultura.Utente'

SITE_ID = 1

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Agora_Cultura.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Agora_Cultura.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validazione delle password
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internazionalizzazione
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# File statici (CSS, JavaScript, Immagini)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# File media (File caricati dagli utenti)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tipo di campo predefinito per la chiave primaria
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurazione delle sessioni
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usa il database per le sessioni
SESSION_COOKIE_AGE = 1209600  # 2 settimane in secondi
SESSION_COOKIE_SECURE = DEBUG is False  # Cookie sicuri in produzione
SESSION_COOKIE_HTTPONLY = True  # Previene l'accesso JavaScript ai cookie di sessione
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Sessioni persistenti
