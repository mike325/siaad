"""
Django settings for siaad project.
Generated by 'django-admin startproject' using Django 1.8.2.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path
import sys
import dj_database_url


DJ_PROJECT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(__file__)
BASE_DIR = Path(__file__).ancestor(2)

#print (" Base dir {0}".format(BASE_DIR))

#BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
WSGI_DIR = None
REPO_DIR = None

#print("Static {0}".format(BASE_DIR.ancestor(1).child("static")))

if os.environ.get('OPENSHIFT_DATA_DIR', "null") != "null":
    WSGI_DIR = BASE_DIR.ancestor(1)
    REPO_DIR = WSGI_DIR
    pass
else:
    WSGI_DIR = BASE_DIR
    REPO_DIR = WSGI_DIR
    pass


DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

#sys.path.append(os.path.join(, 'local_libs'))
sys.path.append(os.path.join(BASE_DIR, 'local_libs'))

if DATA_DIR != BASE_DIR :
    sys.path.append(os.path.join(REPO_DIR, 'libs'))
    pass

sys.path.append(os.path.join(BASE_DIR, 'apps'))

DEBUG = False
ALLOWED_HOSTS = []
SECRET_KEY = None
SECRETS = None 

ADMINS = (('Miguel Ochoa', 'siaad.cucei@prodeveloper.me'),)

# SECURITY WARNING: don't run with debug turned on in production!
if DEBUG is True :
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ALLOWED_HOSTS = ["*"]

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '4%iv7959!4u!$6!v@i^xp&%h2h$d_hs6%9zyf4%=rm_8fp((n('
    pass
else:
    #import local_libs.secrets
    from local_libs.local_getter import *

    from socket import gethostname
    ALLOWED_HOSTS = [
        gethostname(), # For internal OpenShift load balancer security purposes.
        'localhost',
        os.environ.get('OPENSHIFT_APP_DNS', "127.0.0.1"),
        'siaad.herokuapp.com',
        'siaad.prodeveloper.me',
        #'example.com', # First DNS alias (set up in the app)
        #'www.example.com', # Second DNS alias (set up in the app)
    ]

    if os.environ.get('OPENSHIFT_APP_DNS', "null") != "null":
        ALLOWED_HOSTS += os.environ.get('OPENSHIFT_APP_DNS') # Dynamically map to the OpenShift gear name.
        pass


    # SECURITY WARNING: keep the secret key used in production secret!
    #SECRETS = secrets.getter(BASE_DIR.child("secrets.json"))
    SECRETS = getter(os.path.join(DATA_DIR, 'secrets.json'))
    #SECRETS = getter(os.path.join(DATA_DIR, 'secrets.json'))
    SECRET_KEY = SECRETS['secret_key']
    pass

# Application definition

# Aplicaciones de django, de terceros y locales
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = ()
#LOCAL_APPS = ()

#"""
LOCAL_APPS = (
    'apps.Usuarios',
    'apps.Departamentos',
    'apps.Historicos',
    'apps.Reportes',
    'apps.Listas',
)
#"""

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'siaad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'siaad.commons.shortcuts.sidebar_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'siaad.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
#DATABASES = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child('db.administracion.sqlite3'),
    }
}

if 'TRAVIS' in os.environ:
    if os.environ.get('DB') == "mysql":
        DATABASES = {
            'default': {
                'ENGINE':  'django.db.backends.mysql',
                'NAME': 'travis', 
                'USER': 'travis',
                'PASSWORD': '',
                'HOST': 'localhost',
            }
        }
        pass
    elif os.environ.get('DB') == "postgres":
        DATABASES = {
            'default': {
                'ENGINE':  'django.db.backends.postgresql_psycopg2',
                'NAME': 'travis', 
                'USER': 'travis',
                'PASSWORD': '',
                'HOST': 'localhost',
            }
        }
        pass
    pass
elif DEBUG is False:
# Heroku configurations
    #if os.environ.get("DATABASE_URL", "null") != "null":
        #DATABASES['default'] =  dj_database_url.config()
    #    pass
# RedHat OpenShift configurations
    if os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME', "null") != "null":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('OPENSHIFT_GEAR_NAME'),
                'USER': os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME'),
                'PASSWORD': os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD'),
                'HOST': os.environ.get('OPENSHIFT_MYSQL_DB_HOST'),
                'PORT': os.environ.get('OPENSHIFT_MYSQL_DB_PORT'),
            }
        }
        pass
# secrets.json configurations
    elif SECRETS["db_engine"] != 'django.db.backends.sqlite3':
        DATABASES = {
            'default': {
                'ENGINE': SECRETS["db_engine"],
                'NAME': SECRETS["db_name"], 
                'USER': SECRETS["db_user"],
                'PASSWORD': SECRETS["db_password"],
                'HOST': SECRETS["db_host"],
                'PORT': SECRETS["db_port"],
            }
        }
        pass
# Else keep the default sqlite configurations
pass


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps'),
)


if os.environ.get('OPENSHIFT_DATA_DIR', "null") != "null":
    STATIC_ROOT = os.path.join(BASE_DIR, '../static')
    STATICFILES_DIRS += os.path.join(BASE_DIR, 'static')
    pass

#print ("Padre static {0}".format(STATIC_ROOT))

#STATICFILES_DIRS = (BASE_DIR.child('static'),)
#STATIC_ROOT = 'staticfiles'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
