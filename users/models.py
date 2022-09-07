from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from base_app.models import BaseModel


class ApplicationUser(AbstractUser, BaseModel):
    class Meta:
        db_table = 'application_users'
        ordering = ['-create_date']



