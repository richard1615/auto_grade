from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('assignments/', views.AssignmentListView.as_view(), name='assignments'),
    path('assignment/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignment/new/', views.AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignment/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment-delete'),
    path('submissions/', views.SubmissionListView.as_view(), name='submissions'),
    path('submission/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/<int:assignment_id>', views.SubmissionListView.as_view(), name='submissions'),
    path('submission/<int:pk>/delete/', views.SubmissionDeleteView.as_view(), name='submission-delete'),
    path('submission/<int:assignment_id>/new/', views.SubmissionCreateView.as_view(), name='submission-create'),
    path('assignments/sms/<int:user_id>/<int:assignment_id>', views.assignments_sms, name='assignments_sms'),
    path('submissions/sms/<int:user_id>/<int:assignment_id>', views.submissions_sms, name='submissions_sms')
]
