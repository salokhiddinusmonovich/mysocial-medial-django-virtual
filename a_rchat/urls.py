from django.urls import path
from .views import *

urlpatterns = [
    path('', lambda request: redirect('chatroom', chatroom_name='OurChat'), name='home'),
    path('chatroom/<str:chatroom_name>/', chat_view, name='chatroom'),
]