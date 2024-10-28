"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.gingerdj.gloportal.dev/en/4.2/howto/deployment/wsgi/
"""

import os

from gingerdj.core.wsgi import get_wsgi_application

os.environ.setdefault("GINGER_SETTINGS_MODULE", "server.settings")

application = get_wsgi_application()
