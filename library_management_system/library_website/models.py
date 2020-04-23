from django.db import models 
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from PIL import Image
from django.utils import timezone

#Book Model
class Book(models.Model):
	title = models.CharField(max_length = 250)
	author = models.ForeignKey('Author', on_delete=models.CASCADE, null = True) # CASCADE means if a book is deleted, the author won't be deleted
	publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, null = True)
	year_of_publication = models.CharField('Year of Publication', default='', max_length=4 )
	isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')
	dewey = models.CharField('Dewey Decimal System', default='', max_length=3, help_text='3 Digit Call Number based on Book Subject or Genre')
	image = models.ImageField(default='noImage.jpg', upload_to='book_pics', help_text='Upload cover photo of the book')
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('library-book_detail', args=[str(self.id)])


#Author Model
class Author (models.Model):
	first_name = models.CharField(max_length=100, help_text='First name of the Author')
	last_name = models.CharField(max_length=100, help_text='Last name of the Author')

	class Meta: 
		ordering = ['first_name', 'last_name']

	def __str__(self):
		return f'{self.first_name}, {self.last_name}'


#Publisher Model
class Publisher (models.Model):
	publisher_name = models.CharField(max_length=200, help_text='Name of Publisher')

	def __str__(self):
		return self.publisher_name


#Status Model
import uuid  # Required for unique book instances 

class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, help_text='Choose an instance of a book')
	imprint = models.CharField(max_length=200, help_text='Follow this template: Published by [insert author name] on [insert year of publication]')
	due_back = models.DateField(null=True, blank=True, help_text='Follow this template: [YYYY-MM-DD] (Ex.: 2020-04-26) [NOTE: PLEASE LEAVE FIELD AS EMPTY IF THERE IS NO BORROWER]')
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text='[NOTE: PLEASE CHOOSE NULL FIELD IF THERE IS NO BORROWER]')
	
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
		help_text='Book availability [NOTE: PLEASE SET TO AVAILABLE IF BOOK IS NOT BORROWED]',
	)

	class Meta:
		ordering = ['due_back']

	def __str__(self):
		return f'{self.id}'

	def get_absolute_url(self):
		return reverse('library-update_bookInstance', args=[uuid(self.id)])


import uuid  # Required for unique book instances 
class Comment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
	book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	comment = models.TextField(default = '', max_length = 3000, help_text='Enter your review of the book')
	created_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_on']

	def __str__(self):
		return f'{self.id}'
		# return 'Comment {} by {}'.format(self.comment, self.user)