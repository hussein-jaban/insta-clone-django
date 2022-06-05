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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = CloudinaryField('image')
    caption = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    

    class Meta:
      ordering = ['-created']
    def __str__(self):
        return self.user.username
     
     
class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   body = models.TextField()
   created = models.DateTimeField(auto_now_add=True)  
   
   class Meta:
      ordering = ['-created']
      
   def __str__(self):
         return self.body[0:50]
      
      
class AllLikes(models.Model):
   post_id = models.CharField(max_length=200)
   username = models.CharField(max_length=200)
   
   def __str__(self):
         return self.username
      
      
class FollowersCount(models.Model):
   follower = models.CharField(max_length=200)
   user = models.CharField(max_length=200)
   
   def __str__(self):
         return self.user
   
   
   
