"""
ASGI config for my_test_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter 
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_test_site.settings')

# application = get_asgi_application()
# overiding default
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": URLRouter(
      routing.websocket_urlpatterns
  ),
})

