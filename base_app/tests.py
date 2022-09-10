import pytest
from django.test import TestCase

# Create your tests here.
from faker import Faker

from users.models import ApplicationUser

fake = Faker()


@pytest.fixture
def user(db) -> ApplicationUser:
    profile = fake.profile()
    fake_email = fake.email()
    return ApplicationUser.objects.create(username=fake_email, email=fake_email)
