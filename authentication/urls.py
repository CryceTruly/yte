from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', views.RegistrationAPIView.as_view(), name='register'),
    path('api/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/email-verify/', views.EmailVerifyAPIView.as_view(), name='email-verify'),
    path('api/password-reset-request/', views.PasswordResetAPIView.as_view(),
         name='password-reset/'),
    path('api/password-change/<uidb64>/<token>/', views.PasswordResetCompleteAPIView.as_view(),
         name='setnewpassword'),
    path('api/password-reset-complete/', views.PasswordResetCompleteFinalAPIView.as_view(),
         name='complete-setnewpassword'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
