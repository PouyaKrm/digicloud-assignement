from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.views import APIView

from base_app.http_helpers import ok
from base_app.serializers import BaseSerializer
from users.custom_validator import password_validator
from users.selectors import user_exists_by_email

from django.utils.translation import gettext as _

from users.services import register_user


class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    class RegisterSerializer(BaseSerializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(
            min_length=8, max_length=16,
            style={'input_type': 'password', 'write_only': True},
            write_only=True,
            validators=[password_validator]
        )

        def validate_email(self, value):
            if user_exists_by_email(email=value):
                raise ValidationError(_("Email already exists"))
            return value

    def post(self, request: Request):
        sr = self.RegisterSerializer(data=request.data)
        sr.is_valid(True)
        tokens = register_user(**sr.validated_data)
        return ok(tokens)




