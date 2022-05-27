from django import views
from django.urls import path
from .views import RegisterView, VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('email_verify',VerifyEmail.as_view(), name = 'email-verify'),
]
