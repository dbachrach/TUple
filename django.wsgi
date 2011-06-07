import os
import sys

path = '/usr/local/wsgi/'
if path not in sys.path:
    sys.path.append(path)
path = '/usr/local/wsgi/TUple/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'TUple.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

