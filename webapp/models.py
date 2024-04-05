from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime  import datetime



class User(AbstractUser):
    avatar = models.ImageField(null=True)
    image_link = models.TextField(max_length=1000, null=True)
    REQUIRED_FIELDS = []
    

class Complaint(models.Model):
     categories = models.CharField(max_length=200)
     body = models.TextField()
     img = models.ImageField(null=True)
     image_link = models.TextField(max_length=1000, null=True)
     def __str__(self):
         return self.categories