import email
from django.test import TestCase
from base.models import User, Post, Comment


class TestModel(TestCase):
   def test_create_user(self):
    user = User.objects.create_user(username='banana', email='banana@gmail.com', password1='mwas6190', password2='mwas6190')
    user.save()
    
    self.assertEqual(str(user), 'banana')
    
   def test_create_post(self):
    user = User.objects.create_user(username='banana', email='banana@gmail.com', password1='mwas6190', password2='mwas6190')
    user.save()
    post = Post.objects.create(user=user, image='image/upload/v1654464303/dhagnnfxtfd9ldneefvv.jpg', 
                               caption='test image', )
    post.save()
    
    self.assertEqual(str(post), 'banana')
    
   def test_create_comment(self):
    user = User.objects.create_user(username='banana', email='banana@gmail.com', password1='mwas6190', password2='mwas6190')
    user.save()
    post = Post.objects.create(user=user, image='image/upload/v1654464303/dhagnnfxtfd9ldneefvv.jpg', 
                               caption='test image', )
    post.save()
    
    comment = Comment.objects.create(user=user, post=post, body='just commented')
    comment.save()
    self.assertEqual(str(comment), 'just commented')