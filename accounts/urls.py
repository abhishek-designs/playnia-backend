from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up_user, name='sign_up'),
    path('sign_in/', views.sign_in_user, name='sign_in'),
    path('user_profile/', views.fetch_user, name='user_profile'),
    path('update_user/', views.update_user, name='update_user'),
    path('fetch_user/<int:pk>/', views.fetch_user, name='fetch_user')
]