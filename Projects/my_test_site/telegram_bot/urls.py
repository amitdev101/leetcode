from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('telegram_bot/', views.telegram_bot, name='telegram_bot'),
    path('chrome_extension/', views.chrome_extension, name='chrome_extension'),
    path('send_to_telegram/', views.send_to_telegram, name='send_to_telegram')
]
