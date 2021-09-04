from django.db import models

# Create your models here.
class User(models.Model):
    """ユーザーモデル"""
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    point = models.IntegerField(default=0)