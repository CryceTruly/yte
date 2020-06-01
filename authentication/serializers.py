from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from validate_email import validate_email
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            "min_length": "Password should be at least {min_length} characters"
        }
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, value):
        data = self.get_initial()
        email = data.get("email")
        username = data.get("username")

        # validate that username passed is correct
        if not username.isalnum():
            raise serializers.ValidationError(
                "The username is invalid please use letters and numbers")
        self.user_exists('username', username)

        # validate that the correct email format is used
        if not validate_email(email):
            raise serializers.ValidationError("Enter a valid email address.")
        # Validate email has not been used to create account before
        self.user_exists('email', email)
        return value

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)

    def user_exists(self, field, value):
        if(field == 'email' and User.objects.filter(
                email=value).first() is not None):
            raise serializers.ValidationError(
                "This email has already been used to create a user")
        elif User.objects.filter(username=value).first() is not None:
            raise serializers.ValidationError(
                "This username already exists please choose another one")


class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=256, read_only=True)
    tokens = serializers.CharField(max_length=256, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise AuthenticationFailed(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed(
                'Incorrect email password combination,check and try again', 401
            )
        if not user.is_active:
            raise serializers.ValidationError()

        verified_user = User.objects.filter(email=email).first()
        if not verified_user.is_verified:
            raise ValidationError(
                {'email':
                 'Email is not verified please click the link in your mailbox'},
            )
        return {
            'email': user.email,
            'username': user.username,
            'max_idle_time': user.max_idle_time,
            'tokens': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', )

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        # save the model.
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ('email', )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)
    uidb64 = serializers.CharField(
        max_length=128, min_length=1, write_only=True)
    token = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        fields = ('password', 'uidb64', 'token')

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    'The link is invalid,please request a new one', 401
                )

            user.set_password(password)
            user.save()
            return (user)
        except DjangoUnicodeDecodeError as identifier:
            raise serializers.ValidationError(ValidationError(
                {'token': 'invalid token'}))
        return super().validate(attrs)
