from django.shortcuts import render
from django.http import HttpResponse

books = [
    {
        'title': 'Science Book',
        'author': 'Nicolas Sy',
        'publisher': 'Nic Inc.',
        'year_of_publication' : '2009',
        'content': 'book content 1'
    },

    {
        'title': 'Mathematics',
        'author': 'Henric Tay',
        'publisher': 'Hentai Inc.',
        'year_of_publication' : '2010',
        'content': 'book content 2'
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