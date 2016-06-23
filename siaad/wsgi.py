"""
WSGI config for siaad project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siaad.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
"""

import os, sys

if os.environ.get('OPENSHIFT_REPO_DIR', "null") != "null":
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR']))
    pass

os.environ['DJANGO_SETTINGS_MODULE'] = 'siaad.settings'

if os.environ.get('OPENSHIFT_PYTHON_DIR', "null") != "null":

    virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python3.3/site-packages')
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')

    try:
        execfile(virtualenv, dict(__file__=virtualenv))
    except IOError:
        pass

    pass



#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
