from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from library_website.models import BookInstance

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	id_number = models.CharField(default='', max_length=8)

	def __str__(self):
		return f'{self.user.username} Profile'