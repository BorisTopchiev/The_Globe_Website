from django.db import models

class User:
    password = models.CharField()
    login = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)