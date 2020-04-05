from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import BookInstance

# Create your views here.
def home(request):
    context = {
        'books': Book.objects.all(),
        'bookInstances': BookInstance.objects.all()
    }
    return render(request, 'library_website/home.html', context)

def about(request):
    return render(request, 'library_website/about.html', {'title': 'About'})