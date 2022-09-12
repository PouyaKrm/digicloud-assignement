import pytest
from django.test import TestCase

# Create your tests here.
from faker import Faker
from rest_framework.test import APIClient

from users.models import ApplicationUser
from rest_framework_simplejwt.tokens import RefreshToken

fake = Faker()


@pytest.fixture
def user(db) -> ApplicationUser:
    profile = fake.profile()
    fake_email = fake.email()
    return ApplicationUser.objects.create(username=fake_email, email=fake_email)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_authenticated(user):
    api_client = APIClient()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

