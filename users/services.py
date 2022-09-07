from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ApplicationUser


def register_user(*args,  email: str, password: str) -> dict:
    user = ApplicationUser.objects.create(username=email, email=email)
    user.set_password(password)
    user.save()
    return generate_auth_tokens(user=user)


def generate_auth_tokens(*args, user: ApplicationUser):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


