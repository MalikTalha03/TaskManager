from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserData(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Use the built-in User model
    task = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10)
    completion_date = models.DateField()
