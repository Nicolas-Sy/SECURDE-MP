from django import forms
from .models import Book, BookInstance, Author, Publisher, BookInstance

class CreateBook(forms.ModelForm):
	class Meta:
		model = Book 
		fields = ['title', 'year_of_publication', 'isbn']

class CreateAuthor(forms.ModelForm):
	class Meta:
		model = Author
		fields = ['first_name', 'last_name']

class CreatePublisher(forms.ModelForm):
	class Meta:
		model = Publisher 
		fields = ['publisher_name']

class CreateBookInstance(forms.ModelForm):
	class Meta: 
		model = BookInstance
		fields = ['book', 'imprint', 'status', 'due_back', 'borrower']