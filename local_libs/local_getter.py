import json
import os
from unipath import Path

BASE_DIR = Path(__file__).ancestor(2)
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

__secrets = {
    'secret_key': '4%iv7959!4u!$6!v@i^xp&%h2h$d_hs6%9zyf4%=rm_8fp((n(',
    'db_engine': 'django.db.backends.sqlite3',
}

def getter(path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except IOError:
        return __secrets

def generator():
    # Based on Django's SECRET_KEY hash generator
    # https://github.com/django/django/blob/9893fa12b735f3f47b35d4063d86dddf3145cb25/django/core/management/commands/startproject.py
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    __secrets['secret_key'] = get_random_string(50, chars)

    return __secrets

def generator_dev():
    # Based on Django's SECRET_KEY hash generator
    # https://github.com/django/django/blob/9893fa12b735f3f47b35d4063d86dddf3145cb25/django/core/management/commands/startproject.py
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    __secrets['secret_key'] = get_random_string(50, chars)
    __secrets["db_engine"] = 'django.db.backends.sqlite3'

    with open(BASE_DIR.child('secrets.json'), "w") as ACCESS:
        json.dump(__secrets, ACCESS)
        pass
    return __secrets
    pass

def generator_production():
    # Based on Django's SECRET_KEY hash generator
    # https://github.com/django/django/blob/9893fa12b735f3f47b35d4063d86dddf3145cb25/django/core/management/commands/startproject.py
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    __secrets['secret_key'] = get_random_string(50, chars)

    #__secrets["db_engine"] = 'django.db.backends.mysql'

    """
    Running on production the user should set the following values.

    You can run the script first with generator_dev() function and
    later add these values in the secrets.json file.
    """

    __secrets["db_name"] = ""
    __secrets["db_user"] = ""
    __secrets["db_password"] = ""
    __secrets["db_host"] = ""
    __secrets["db_port"] = ""

    with open(BASE_DIR.child('secrets.json'), "w") as ACCESS:
        json.dump(__secrets, ACCESS)
        pass
    return __secrets
    pass

if __name__ == '__main__':
    data = json.dumps(generator_production())
    print(data)
