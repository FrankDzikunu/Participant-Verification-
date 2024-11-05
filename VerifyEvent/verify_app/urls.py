from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', auth_views.LoginView.as_view(template_name='verify_app/admin_login.html'), name='login'),
    path('', views.verify_participant, name='verify_participant'),
    path('manage/', views.manage_participants, name='manage_participants'),
    path('verify/<int:participant_id>/', views.toggle_verification, name='toggle_verification'),  # New URL for updating verification status
]
