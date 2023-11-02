from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('receive/', views.receive_command, name='browser_receive'),
    path('send/', views.send_command, name='browser_send')
]
