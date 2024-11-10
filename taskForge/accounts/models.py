from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

from taskForge.accounts.choices import UserRoleChoices


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email or not password:
            raise ValidationError('Email and password are required')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=email
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=150, unique=True)

    objects = CustomUserManager()

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices,
        default='end_user'
    )

    def __str__(self):
        return f'{self.user.first_name}\'s Profile'

