from django.forms import ModelForm
from base.models import User
from django.contrib.auth.forms import UserCreationForm




class MyCreateUserForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
   super().__init__(*args, **kwargs)
   self.fields['username'].widget.attrs.update({'type': 'text', 'placeholder': 'Username'})
   self.fields['email'].widget.attrs.update({'type': 'email', 'placeholder': 'Email'})
   self.fields['password1'].widget.attrs.update({'type': 'password', 'placeholder': 'Password'})
   self.fields['password2'].widget.attrs.update({'type': 'password', 'placeholder': 'Confirm Password'})
  class Meta:
   model = User
   fields = ['username', 'email', 'password1', 'password2']