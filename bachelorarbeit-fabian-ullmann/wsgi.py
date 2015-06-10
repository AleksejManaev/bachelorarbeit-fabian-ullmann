"""
WSGI config for untitled project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

# import os
# # activate virtualenv
# activate_this = os.path.expanduser("/var/www/bachelorarbeit/ba-2.7.10/bin/activate_this.py")
# execfile(activate_this, dict(__file__=activate_this))
#
# import sys
#
# import os
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bachelorarbeit-fabian-ullmann.settings")
#
# application = get_wsgi_application()

# import os
# import sys
#
# # activate venv
# activate_this = '/var/www/bachelorarbeit/ba-2.7.10/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
#
# # insert project path to sys path
# path = '/var/www/bachelorarbeit/ba-2.7.10/'
# if path not in sys.path:
#     sys.path.insert(0, path)

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bachelorarbeit-fabian-ullmann.settings")

application = get_wsgi_application()