from rest_framework import status, generics, serializers, views
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetPasswordSerializer, EmailVerifySerializer, ChangePasswordSerializer
)
import jwt
from .utils import Utilities
from .permissions import IsOwner

from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        email = user_data['email']
        created_user = User.objects.get(email=email)
        token = RefreshToken.for_user(created_user).access_token
        message = [
            request,
            "verify",
            token,
            "Confirm Your Email Address",
            email
        ]

        Utilities.send_email(message, None, 'auth')

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserInfoAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwner)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerifyAPIView(views.APIView):
    serializer_class = EmailVerifySerializer

    token_param = openapi.Parameter('token', in_=openapi.IN_QUERY, description='token',
                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.exceptions.DecodeError:
            return self.send_response("verification link is invalid")
        except jwt.ExpiredSignatureError:
            return self.send_response("verification link is expired")
        user = User.objects.filter(id=payload.get('user_id')).first()
        if not user.is_verified:
            user.is_verified = True
            user.save()
        return self.send_response('Account activation successfull', status=status.HTTP_200_OK)

    def send_response(self, message, status=status.HTTP_400_BAD_REQUEST):
        return Response({"message": message}, status)


class PasswordResetAPIView(generics.GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    # then send rest password link
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        domain = request.META.get(
            'HTTP_ORIGIN', get_current_site(request).domain)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.filter(email=request.data['email'])
            if not user:
                raise serializers.ValidationError({
                    "email": ["No records correspondingly this user were found"]
                })

            uidb64 = urlsafe_base64_encode(smart_bytes(user[0].id))
            token = PasswordResetTokenGenerator().make_token(user[0])

            message = [
                request,
                reverse('authentication:setnewpassword', kwargs={
                        "uidb64": uidb64, "token": token}),
                "Reset Password",
                "Reset Password",
                request.data['email']
            ]

            Utilities.send_email(message, domain, 'password_reset')
            return Response(
                {
                    "message":
                    "Please check your email for the reset password link."
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return Response({
                "errors": {
                    "email": ["Email is required to reset a password"]
                }},
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetCompleteAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None or not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'errors': [
                {'token': 'Link is not valid,please request a new one'}

            ]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': {"message": 'Credentials Valid', 'uidb64': uidb64, 'token': token}}, status=status.HTTP_200_OK)


class PasswordResetCompleteFinalAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    renderer_classes = (UserJSONRenderer,)
    permission_classes = (AllowAny,)

    def patch(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return self.send_response('Password changed successfully,login with your new password', status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return self.send_response('Something went wrong,you could not update your password', status=status.HTTP_401_UNAUTHORIZED)

    def send_response(self, message, status=status.HTTP_400_BAD_REQUEST):
        return Response({"message": message}, status)
