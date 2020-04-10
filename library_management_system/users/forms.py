from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

	def save(self, commit = True):
		user = super().save(commit=False)

		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_lane = self.cleaned_data['last_name']

		if commit: 
			user.save()
		return user 

class UserUpdateForm(forms.ModelForm):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']	

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['id_number', 'image']

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = Profile 
		fields = ['id_number']