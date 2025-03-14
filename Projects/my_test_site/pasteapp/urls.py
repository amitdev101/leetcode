from django.urls import path, re_path
from .views import formatter_view, paste_page

urlpatterns = [
    path("paste/", paste_page, name="paste"),
    re_path(r'^(?:(?P<room_id>[\w-]+))?/?$', formatter_view, name="formatter"),
]
