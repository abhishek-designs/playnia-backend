from django.urls import path
from . import views

urlpatterns = [
    path('create_lobby/', views.create_lobby, name='create_lobby'),
    path('fetch_lobbies/', views.fetch_lobbies, name='fetch_lobbies'),
    path('fetch_lobbies/<int:pk>/', views.fetch_lobby, name='fetch_lobby'),
]