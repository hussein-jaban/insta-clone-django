from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
import uuid


# Create your models here.
class User(AbstractUser):
   name = models.CharField(max_length=200, null=True)
   email = models.EmailField(unique=True)
   bio = models.TextField(null=True)
   image = CloudinaryField('image', null=True, blank=True, default='image/upload/v1654285390/hz7a08c74kynhnx24lwd.png')
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']
   
   
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = CloudinaryField('image')
    caption = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    class Meta:
      ordering = ['-created']
    def __str__(self):
        return self.user
   
   
