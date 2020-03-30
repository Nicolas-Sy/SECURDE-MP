from django.shortcuts import render
from django.http import HttpResponse

books = [
    {
        'title': 'Science Book',
        'author': 'Nicolas Sy',
        'publisher': 'Nic Inc.',
        'year_of_publication' : '2009'
    },
{
        'title': 'Mathematics',
        'author': 'Sean Sy',
        'publisher': 'Sean Inc.',
        'year_of_publication' : '2010'
    },
]

# Create your views here.
def home(request):
    context = {
        'books': books
    }
    return render(request, 'library_website/home.html', context)

def about(request):
    return render(request, 'library_website/about.html', {'title': 'About'})