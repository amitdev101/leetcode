from django.urls import path
from . import views

urlpatterns = [
    path('set/<str:key>/', views.store_data, name='store-data'),
    path('get/<str:key>/', views.get_data, name='get-data'),
    path('delete/<str:key>/', views.delete_data, name='delete-data'),
    path('chat/', views.index, name='chat-stream-data')
]
