from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    age = models.IntegerField()
    password = models.CharField(max_length=100)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []










