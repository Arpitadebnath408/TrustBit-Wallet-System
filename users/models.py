from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)
    address = models.CharField(max_length=255)