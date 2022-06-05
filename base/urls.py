from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutUser, name='logout'),
    path('accountSettings/', views.accountSettings, name='accountSettings'),
    path('uploadPic/', views.uploadPic, name='uploadPic'),
    path('post/<pk>/', views.post, name='post'),
    
]