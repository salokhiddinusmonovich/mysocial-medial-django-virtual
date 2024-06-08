from django.urls import path
from .views import *

urlpatterns = [
    path('', lambda request: redirect('chatroom', chatroom_name='OurChat'), name='home'),
]