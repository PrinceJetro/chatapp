from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime  import datetime



class User(AbstractUser):
    avatar = models.ImageField(null=True)
    image_link = models.TextField(max_length=1000, null=True)
    REQUIRED_FIELDS = []
    

class Complaint(models.Model):
     categories = models.CharField(max_length=2000)
     body = models.TextField(max_length=10000)
     img = models.ImageField(null=True)
     image_link = models.TextField(max_length=5000, null=True)
     def __str__(self):
         return self.categories


class OnlineClass(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)  # Changed to CharField
    more = models.TextField()

    def __str__(self):
        return self.full_name
