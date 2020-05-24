from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('email-verify/', views.EmailVerifyAPIView.as_view(), name='email-verify'),
    path('password-reset-request/', views.PasswordResetAPIView.as_view(),
         name='password-reset/'),
    path('password-change/<uidb64>/<token>/', views.PasswordResetCompleteAPIView.as_view(),
         name='setnewpassword'),
    path('password-reset-complete/', views.PasswordResetCompleteFinalAPIView.as_view(),
         name='complete-setnewpassword'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
