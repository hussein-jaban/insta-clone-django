from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
   name = models.CharField(max_length=200, null=True)
   email = models.EmailField(unique=True)
   bio = models.TextField(null=True)
   image = CloudinaryField('image', null=True, blank=True, default='image/upload/v1654285390/hz7a08c74kynhnx24lwd.png')
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']