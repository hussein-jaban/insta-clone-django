import email
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from base.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from base.forms import MyCreateUserForm
from django.core.mail import send_mail



# Create your views here.
@login_required(login_url='loginPage')
def home(request):
   if request.method == 'POST':
     email = request.POST['email']
     
   return render(request, 'home.html')
  
  
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
