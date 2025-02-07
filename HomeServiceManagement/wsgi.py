"""
WSGI config for Home360 project.

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HomeServiceManagement.settings')

application = get_wsgi_application()
