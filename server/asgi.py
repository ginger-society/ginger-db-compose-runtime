"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.gingerdj.gloportal.dev/en/4.2/howto/deployment/asgi/
"""

import os

from gingerdj.core.asgi import get_asgi_application

os.environ.setdefault("GINGER_SETTINGS_MODULE", "server.settings")

application = get_asgi_application()
