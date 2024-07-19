from django.urls import path

from a_users.views import profile_view
from .views import *

urlpatterns = [
    path('', messageboard_view, name="messageboard"),
    path('subscribe/', subscripe, name="subscribe")

]
