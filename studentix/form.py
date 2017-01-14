from django.forms import ModelForm
from django import forms
from . import models
from django.db import models
from django.contrib.auth.models import User


class SignupForm(ModelForm):
	dob = forms.DateField(label='Date of Birth')
	contact = forms.CharField(max_length=10);
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password',]
		widgets = {
            'password': forms.PasswordInput(),
        }
		

		
class ParentForm(forms.Form):
	dob = forms.DateField(label='Date of Birth')
	username = forms.CharField(max_length=100)	
