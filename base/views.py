from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from base.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
   return render(request, 'home.html')
  
  
def loginPage(request):
   if request.method == 'POST':
     email = request.POST['email']
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
