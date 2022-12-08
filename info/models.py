from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    dt_created = models.DateTimeField(auto_now_add=True)


class DevTeam(models.Model):
    username = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

