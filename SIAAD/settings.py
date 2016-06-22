"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

DEBUG = os.environ.get('DEBUG') == 'True'

ADMINS = (('Miguel Ochoa', 'siaad.cucei@prodeveloper.me'),)

import sys
sys.path.append(os.path.join(REPO_DIR, 'libs'))
sys.path.append(os.path.join(BASE_DIR, 'apps'))
import secrets
SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None 

if DEBUG is True :
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ALLOWED_HOSTS = ["*"]

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '4%iv7959!4u!$6!v@i^xp&%h2h$d_hs6%9zyf4%=rm_8fp((n('
    pass
else:
    import secrets

    from socket import gethostname
    ALLOWED_HOSTS = [
        gethostname(), # For internal OpenShift load balancer security purposes.
        'siaad.herokuapp.com',
        'siaad.prodeveloper.me',
        #'example.com', # First DNS alias (set up in the app)
        #'www.example.com', # Second DNS alias (set up in the app)
    ]

    # SECURITY WARNING: keep the secret key used in production secret!
    #SECRETS = secrets.getter(BASE_DIR.child("secrets.json"))
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
)

# GETTING-STARTED: change 'myproject' to your project name:
ROOT_URLCONF = 'SIAAD.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'SIAAD.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.administracion.sqlite3'),
    }
}

if DEBUG is False:
    # Heroku configurations
    if os.environ.get("DATABASE_URL", "null") != "null":
        # sqlite uses the dyno space which is more than the
        # postgresql free instance ( 7.2 mb vs ~230 mb )
        # DATABASES['default'] =  dj_database_url.config()
        pass
    # RedHat OpenShift configurations
    elif os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME', "null") != "null":
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WSGI_DIR, 'static')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
