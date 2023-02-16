from django.forms import ModelForm
from .models import Donation
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DonationForm(ModelForm):
  class Meta:
    model = Donation
    fields = ['name', 'amount', 'message']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
          'username': None,
          'password1': None,
          'password2': None,
        }

    def __init__(self, *args, **kwargs):
      super(SignUpForm, self).__init__(*args, **kwargs)
      for field_name in ('username', 'email', 'password1', 'password2'):
        self.fields[field_name].help_text = ''
