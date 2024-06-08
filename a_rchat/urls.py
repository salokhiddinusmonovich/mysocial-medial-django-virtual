from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name="chatting"),
    path('', lambda request: redirect('chatroom', chatroom_name='OurChat'), name='home'),
]