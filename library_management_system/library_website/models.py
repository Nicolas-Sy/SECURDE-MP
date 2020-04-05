from django.db import models 
from django.contrib.auth.models import User

#Book Model
class Book(models.Model):
	title = models.CharField(max_length = 250)
	author = models.ForeignKey('Author', on_delete=models.CASCADE) # CASCADE means if a book is deleted, the author won't be deleted
	publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
	year_of_publication = models.DateField(null=True, blank=True)
	isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')
	reviews = models.TextField(max_length = 1000, help_text='Enter your review of the book') #dapat sa user din siya???

	def __str__(self):
		return self.title


#Author Model
class Author (models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)

	class Meta: 
		ordering = ['first_name', 'last_name']

	def __str__(self):
		return f'{self.first_name}, {self.last_name}'


#Publisher Model
class Publisher (models.Model):
	publisher_name = models.CharField(max_length=200)

	def __str__(self):
		return self.publisher_name


#Status Model
import uuid  # Required for unique book instances 

class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = (
		('a', 'Available'),
		('r', 'Reserved'),
	)

	status = models.CharField(
		max_length=1,
		choices=LOAN_STATUS, 
		blank=True,
		default='a',
		help_text='Book availability',
	)

	class Meta:
		ordering = ['due_back']

	def __str__(self):
		return f'{self.id} ({self.book.title})'