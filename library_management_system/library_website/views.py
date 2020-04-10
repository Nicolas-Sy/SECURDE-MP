from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import BookInstance
from .models import Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
    
def home(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'books': Book.objects.all(),
        'bookInstances': BookInstance.objects.all(),
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'library_website/home.html', context)

def about(request):
    return render(request, 'library_website/about.html', {'title': 'About'})

def books(request):
    context = {
        'books': Book.objects.all(),
        'bookInstances': BookInstance.objects.all(),
    }

class BookDetailView(generic.DetailView):
    model = Book