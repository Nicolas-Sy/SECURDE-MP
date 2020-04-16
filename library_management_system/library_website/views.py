from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book
from .models import BookInstance
from .models import Author
from .models import Publisher
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import allowed_users, bookmanager_only
from django.contrib.auth.models import Group
from django import template
from .forms import CreateBook, CreateAuthor, CreatePublisher, CreateBookInstance
from django.contrib import messages


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

@allowed_users(allowed_roles=['BookManager'])
#@bookmanager_only
def about(request):
    return render(request, 'library_website/about.html', {'title': 'About'})


def books(request):
    context = {
        'books': Book.objects.all(),
        'bookInstances': BookInstance.objects.all(),
    }


class BookDetailView(generic.DetailView):
    model = Book


register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, BookManager):
    group =  Group.objects.get(name=BookManager) 
    return group in user.groups.all() 


def createBook(request):
    if request.method == 'POST':
        book_form = CreateBook(request.POST)
        author_form = CreateAuthor(request.POST)
        publisher_form = CreatePublisher(request.POST)

        if book_form.is_valid() and author_form.is_valid() and publisher_form.is_valid():
            author = author_form.save()
            publisher =  publisher_form.save()

            book = book_form.save(commit=False)
            book.author = author
            book.publisher = publisher 
            book.save()
            
            messages.success(request, f'Your book has been created!')
            return redirect('/createBookInstance')

    else:
        book_form = CreateBook()
        author_form = CreateAuthor()
        publisher_form = CreatePublisher()

    context = {
        'book_form': book_form,
        'author_form': author_form,
        'publisher_form': publisher_form,
    }
    return render(request, 'library_website/create_book.html', context)


def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    author = Author.objects.get(id=book.author.id)
    publisher = Publisher.objects.get(id=book.publisher.id)

    book_form = CreateBook(instance=book)
    author_form = CreateAuthor(instance=author)
    publisher_form = CreatePublisher(instance=publisher)

    if request.method == 'POST':
         book_form = CreateBook(request.POST, instance=book)
         author_form = CreateAuthor(request.POST, instance=author)
         publisher_form = CreatePublisher(request.POST, instance=publisher)

         if book_form.is_valid() and author_form.is_valid() and publisher_form.is_valid():
            author = author_form.save()
            publisher =  publisher_form.save()

            bookEdit = book_form.save(commit=False)
            bookEdit.author = author
            bookEdit.publisher = publisher 
            bookEdit.save()
            
            messages.success(request, f'Your book has been edited!')
            return redirect('/')

    context = {
        'book_form': book_form,
        'author_form': author_form,
        'publisher_form': publisher_form,
    }
    return render(request, 'library_website/edit_book.html', context)


def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    author = Author.objects.get(id=book.author.id)
    publisher = Publisher.objects.get(id=book.publisher.id)

    if request.method == 'POST':
        book.delete()
        author.delete()
        publisher.delete()

        messages.success(request, f'Your book has been deleted!')
        return redirect('/')

    context = {
        'book': book,
        'author': author,
        'publisher': publisher,
    }
    return render(request, 'library_website/delete_book.html', context)


def createBookInstance(request):
    if request.method == 'POST':
        book_instance = CreateBookInstance(request.POST)

        if book_instance.is_valid(): 
            book_instance.save()
            
            messages.success(request, f'Your book instance has been created!')
            return redirect('/')

    else:
        book_instance = CreateBookInstance()

    context = {
        'book_instance': book_instance,
    }
    return render(request, 'library_website/create_bookInstance.html', context)


def updateBookInstance(request, pk):
    book_instance = BookInstance.objects.get(id=pk)

    book_instance_form = CreateBookInstance(instance=book_instance)

    if request.method == 'POST':
        book_instance_form = CreateBookInstance(request.POST, instance=book_instance)

        if book_instance_form.is_valid(): 
            book_instance_form.save()
            
            messages.success(request, f'Your book instance has been updated!')
            return redirect('/')

    context = {
        'book_instance_form': book_instance_form
    }

    return render(request, 'library_website/edit_bookInstance.html', context)


def deleteBookInstance(request, pk):
    book_instance = BookInstance.objects.get(id=pk)
    book_title = book_instance.book.title

    if request.method == 'POST':
        book_instance.delete()

        messages.success(request, f'Your book instance has been deleted!')
        return redirect('/')

    context = {
        'book_instance': book_instance,
        'book_title' : book_title
    }
    return render(request, 'library_website/delete_bookInstance.html', context)