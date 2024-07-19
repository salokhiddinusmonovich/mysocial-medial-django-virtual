from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
     path('profile/<str:username>/', views.profile_view, name='profile_prr'),
]
