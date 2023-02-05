from django.urls import path
from . import views

urlpatterns = [
    path('register/<str:user_type>/', views.register, name='register'),
]
