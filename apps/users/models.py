"""
apps/users/models.py
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    currency = models.CharField(max_length=10, default='USD')
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} <{self.email}>"

    @property
    def full_name(self):
        return self.get_full_name() or self.username
