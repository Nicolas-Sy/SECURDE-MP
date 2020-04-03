from django.db import models 
from django.contrib.auth.models import User 


class Book(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	year_of_publication = models.CharField(max_length = 100)

