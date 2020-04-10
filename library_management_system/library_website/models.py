from django.db import models 
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from PIL import Image

#Book Model
class Book(models.Model):
	title = models.CharField(max_length = 250)
	author = models.ForeignKey('Author', on_delete=models.CASCADE) # CASCADE means if a book is deleted, the author won't be deleted
	publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
	year_of_publication = models.DateField(null=True, blank=True)
	isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')
	reviews = models.TextField(max_length = 1000, help_text='Enter your review of the book') #dapat sa user din siya???
	image = models.ImageField(default='default.jpg', upload_to='book_pics')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('library-book_detail', args=[str(self.id)])


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
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	@property
	def is_overdue(self):
	    if self.due_back and date.today() > self.due_back:
	        return True
	    return False
    
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