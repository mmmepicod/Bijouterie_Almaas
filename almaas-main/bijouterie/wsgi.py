"""
plate-forme principale de déploiement Django, selon le standard WSGI ( Standard python pour
les appli et serveurs web

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bijouterie.settings")

application = get_wsgi_application()
