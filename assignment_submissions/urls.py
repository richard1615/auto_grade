from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssignmentListView.as_view(), name='assignments'),
    path('assignment/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),

]
