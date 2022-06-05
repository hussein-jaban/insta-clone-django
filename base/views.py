import email
from email.mime import image
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import context
from base.models import AllLikes, FollowersCount, User, Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from base.forms import MyCreateUserForm
from django.core.mail import send_mail
from cloudinary.forms import cl_init_js_callbacks


# Create your views here.
@login_required(login_url='loginPage')
def home(request):
   posts = Post.objects.all()
   allLikes = AllLikes.objects.all()
   context = {'posts':posts, 'allLikes':allLikes}
   return render(request, 'home.html', context)
  
  
def loginPage(request):
   if request.user.is_authenticated:
     return redirect('home')
   if request.method == 'POST':
     email = request.POST['email'].lower()
     password = request.POST['password']
     print(email)
     print(password)
     try:
         user = User.objects.get(email=email)
     except:
         messages.error(request, 'User not exist.')
         
     user = authenticate(request, email=email, password=password)
     if user:
         login(request, user)
         messages.success(request, 'Log-in Successfull.')
         return redirect('home')
     else:
         messages.error(request, 'Email and password correct.')
   return render(request, 'login.html')
  
  
def logoutUser(request):
    logout(request)
    return redirect('loginPage')
   
def registerPage(request):
    if request.user.is_authenticated:
       return redirect('home')
    form = MyCreateUserForm()
    context = {'form':form}
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']).exists():
          messages.info(request, 'Username is taken')
          return redirect('registerPage')
        elif User.objects.filter(email=request.POST['email']).exists():
          messages.info(request, 'Email is taken')
          return redirect('registerPage')
        elif request.POST['password1'] != request.POST['password2']:
          messages.info(request, 'Password and Confirm Paswword dont match')
          return redirect('registerPage')
        else:
           form = MyCreateUserForm(request.POST)
           if form.is_valid():
               user = form.save(commit=False)
               user.username = user.username.lower()
               user.email = user.email.lower()
               user.save()
               send_mail(
                       f'Hello, {user.username.upper()}', # subject
                       'You are very welcome to ower insta clone app', # body
                       'bazub702@gmail.com', # from email
                       [user.email], # to email
                      )
               login(request, user)
               return redirect('home')
           else:
             messages.error(request, 'An error ocurred during registration.')
          
    return render(request, 'register.html', context)

@login_required(login_url='loginPage')
def accountSettings(request):
  
    if request.method == 'POST':
      username = request.POST.get('username').lower()
      bio = request.POST.get('bio')
      image = request.FILES.get('image')
      print(username, bio, image)

      if User.objects.filter(username=username).exists():
          messages.info(request, 'Username is taken')
          return redirect('accountSettings')
      else:
        user = request.user
        if image != None:
          user.username = username
          user.bio = bio
          user.image = image
          user.save()
        else:
          user.username = username
          user.bio = bio
          user.save()
        return redirect('accountSettings')
          
      
    return render (request, 'account_settings.html')
  
  
@login_required(login_url='loginPage')
def uploadPic(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        print(image)
        print(caption)
        new_post = Post.objects.create(user=request.user, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    return HttpResponse('upload')
  
@login_required(login_url='loginPage')
def post(request, pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all().order_by('-created')
    liked_post = ''
    if request.method == 'POST':
        print(request.POST.get('body'))
        comment = Comment.objects.create(
            user = request.user,
            post = post,
            body = request.POST.get('body')
        )
        post.comments = post.comments + 1
        post.save()
        return redirect('post', pk=post.id)
    username = request.user.username
    post = Post.objects.get(id=pk)
    like_filter = AllLikes.objects.filter(post_id=pk, username=username).first()
    if like_filter == None:
        liked_post = 'img/icon/like-nofill.png'
    else:
        liked_post = 'img/icon/like-fill.png'
    context = {'post':post, 'post_comments':post_comments, 'liked_post':liked_post}   
    return render(request, 'post.html', context)
  
@login_required(login_url='loginPage')
def likePost(request, pk):
    username = request.user.username
    post = Post.objects.get(id=pk)
    
    like_filter = AllLikes.objects.filter(post_id=pk, username=username).first()
    if like_filter == None:
        new_like = AllLikes.objects.create(post_id=pk, username=username)
        new_like.save()
        post.likes = post.likes + 1
        post.save()
    else:
        like_filter.delete()
        post.likes = post.likes - 1
        post.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='loginPage')
def profile(request, pk):
    user = User.objects.get(username=pk)
    posts = Post.objects.filter(user__username=pk)
    post_len = len(posts)
    follower = request.user.username
    current_following = pk
    btn_text = ''
    if FollowersCount.objects.filter(follower=follower, user=current_following).first():
        btn_text = 'Unfollow'
    else:
        btn_text = 'Follow'
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_followings = len(FollowersCount.objects.filter(follower=pk))
    context = {'user': user, 'posts': posts, 
               'post_len':post_len, 'btn_text':btn_text, 
               'user_followers':user_followers, 'user_followings':user_followings}
    return render(request, 'profile.html', context)

@login_required(login_url='loginPage')
def follow(request, pk):
    user_object = User.objects.get(username= pk)
    user = user_object.username
    follower = request.user.username
    print(user)
    print(follower)
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        delete_follower = FollowersCount.objects.get(follower=follower, user=user)
        delete_follower.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        new_follower = FollowersCount.objects.create(follower=follower, user=user)
        new_follower.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))