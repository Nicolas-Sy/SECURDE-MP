from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	firstName = forms.CharField(max_length=100)
	lastName = forms.CharField(max_length=100)
	email = forms.EmailField()
	iDNumber = forms.IntegerField()

	class Meta:
		model = User
		fields = ['firstName', 'lastName', 'username', 'email', 'password1', 'password2', 'iDNumber']

class UserUpdateForm(forms.ModelForm):
	firstName = forms.CharField(max_length=100)
	lastName = forms.CharField(max_length=100)
	email = forms.EmailField()
	iDNumber = forms.IntegerField()

	class Meta:
		model = User
		fields = ['firstName', 'lastName', 'username', 'email', 'iDNumber']	

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

