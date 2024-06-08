from django.urls import path
from django.shortcuts import redirect
from .views import chat_view

urlpatterns = [
    path('', lambda request: redirect('chatroom', chatroom_name='OurChat'), name='home'),
    path('chatroom/<str:chatroom_name>/', chat_view, name='chatroom'),
]
