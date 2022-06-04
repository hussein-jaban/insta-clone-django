from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutUser, name='logout'),
    
]