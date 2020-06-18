from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, BookInstance, Author, Publisher, Comment, HistoryOfBorrowers
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import allowed_users, bookmanager_only, user_is_admin
from django.contrib.auth.models import Group
from django import template
from .forms import CreateBook, CreateAuthor, CreatePublisher, CreateBookInstance, CreateComment
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import F

@user_is_admin
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

@user_is_admin
#@bookmanager_only
def about(request):
    return render(request, 'library_website/about.html', {'title': 'About'})

@user_is_admin
def books(request):
    context = {
        'books': Book.objects.all(),
        'bookInstances': BookInstance.objects.all(),
    }

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, BookManager):
    group =  Group.objects.get(name=BookManager) 
    return group in user.groups.all() 


@allowed_users(allowed_roles=['BookManager'])
def createBook(request):
    if request.method == 'POST':
        book_form = CreateBook(request.POST, request.FILES)
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


@allowed_users(allowed_roles=['BookManager'])
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    author = Author.objects.get(id=book.author.id)
    publisher = Publisher.objects.get(id=book.publisher.id)

    book_form = CreateBook(instance=book)
    author_form = CreateAuthor(instance=author)
    publisher_form = CreatePublisher(instance=publisher)

    if request.method == 'POST':
         book_form = CreateBook(request.POST, request.FILES, instance=book)
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
            return redirect('/book/' + str(book.id))

    context = {
        'book_form': book_form,
        'author_form': author_form,
        'publisher_form': publisher_form,
    }
    return render(request, 'library_website/edit_book.html', context)


@allowed_users(allowed_roles=['BookManager'])
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


@allowed_users(allowed_roles=['BookManager'])
def createBookInstance(request):
    if request.method == 'POST':
        book_instance = CreateBookInstance(request.POST)
        bookID = book_instance.book.id

        if book_instance.is_valid(): 
            book_instance.save()
            
            messages.success(request, f'Your book instance has been created!')
            return redirect('/book/' + str(bookID))

    else:
        book_instance = CreateBookInstance()

    context = {
        'book_instance': book_instance,
    }
    return render(request, 'library_website/create_bookInstance.html', context)


@allowed_users(allowed_roles=['BookManager'])
def updateBookInstance(request, pk):
    book_instance = BookInstance.objects.get(id=pk)
    bookID = book_instance.book.id

    book_instance_form = CreateBookInstance(instance=book_instance)

    if request.method == 'POST':
        book_instance_form = CreateBookInstance(request.POST, instance=book_instance)

        if book_instance_form.is_valid(): 
            book_instance_form.save()
            
            messages.success(request, f'Your book instance has been updated!')
            return redirect('/book/' + str(bookID))

    context = {
        'book_instance_form': book_instance_form
    }

    return render(request, 'library_website/edit_bookInstance.html', context)


@allowed_users(allowed_roles=['BookManager'])
def deleteBookInstance(request, pk):
    book_instance = BookInstance.objects.get(id=pk)
    book_title = book_instance.book.title
    bookID = book_instance.book.id

    if request.method == 'POST':
        book_instance.delete()

        messages.success(request, f'Your book instance has been deleted!')
        return redirect('/book/' + str(bookID))

    context = {
        'book_instance': book_instance,
        'book_title' : book_title
    }
    return render(request, 'library_website/delete_bookInstance.html', context)


@allowed_users(allowed_roles=['Student/Teacher'])
def borrowBookInstance(request, pk):
    book_instance = BookInstance.objects.get(id=pk)
    book_title = book_instance.book.title
    dueback = book_instance.due_back
    borrower = book_instance.borrower
    status = book_instance.status 

    if request.method == 'POST':
        BookInstance.objects.filter(id=book_instance.id).update(due_back=datetime.now() + timedelta(days = 7))
        BookInstance.objects.filter(id=book_instance.id).update(borrower=request.user)
        BookInstance.objects.filter(id=book_instance.id).update(status='r')

        history = HistoryOfBorrowers.objects.create()
        history.book = book_instance.book
        history.borrower = request.user
        history.save()

        messages.success(request, f'You have 7 days from now to return this book. Thank you!')
        return redirect('/')


    context = {
        'book_instance' : book_instance,
        'book_title' : book_title,
    }
    return render(request, 'library_website/borrowBook.html', context)


@allowed_users(allowed_roles=['Student/Teacher'])
def returnBookInstance(request, pk):
    book_instance = BookInstance.objects.get(id=pk)
    book_title = book_instance.book.title
    dueback = book_instance.due_back
    borrower = book_instance.borrower
    status = book_instance.status 
    datenow = datetime.now()

    if request.method == 'POST':
        BookInstance.objects.filter(id=book_instance.id).update(due_back=None)
        BookInstance.objects.filter(id=book_instance.id).update(borrower=None)
        BookInstance.objects.filter(id=book_instance.id).update(status='a')
            
        messages.success(request, f'You have successfully returned this book. Thank you!')
        return redirect('/')

    context = {
        'book_instance' : book_instance,
        'book_title' : book_title,
        'dueback' : dueback,
        'datenow' : datenow
    }
    return render(request, 'library_website/returnBook.html', context)


@user_is_admin
def bookDetail(request, pk):
    book = Book.objects.get(id=pk)
    comments = Comment.objects.filter(book = book)

    if request.method == "POST":
        comment_user = request.user 
        comment_book = book
        comment_form = CreateComment(data=request.POST)

        if comment_form.is_valid():
            finalcomment = comment_form.save(commit=False)
            finalcomment.user = comment_user
            finalcomment.book = comment_book
            finalcomment.save()

            messages.success(request, f'Your review has been posted!')
            comment_form = CreateComment()

    else:
        comment_form = CreateComment()

    context = {
        "book": book,
        "comments" : comments,
        "comment_form": comment_form,
    }

    return render(request, "library_website/book_detail.html", context)

@allowed_users(allowed_roles=['Student/Teacher'])
def editComment(request, pk):
    comments = Comment.objects.get(id=pk)
    bookID = comments.book.id

    editCommentForm = CreateComment(instance=comments)

    if request.method == "POST":
        editCommentForm = CreateComment(request.POST, instance=comments)

        if editCommentForm.is_valid(): 
            editCommentForm.save()
            
            messages.success(request, f'Your comment has been updated!')
            return redirect('/book/' + str(bookID))


    context = {
        "comments" : comments,
        "editCommentForm" : editCommentForm,
    }
    return render(request, "library_website/edit_Comment.html", context)


@allowed_users(allowed_roles=['Student/Teacher'])
def deleteComment(request, pk):
    comments = Comment.objects.get(id=pk)
    commentContent = comments.comment
    commentBook = comments.book
    commentCreatedOn = comments.created_on
    bookID = comments.book.id

    if request.method == "POST":
        comments.delete()
            
        messages.success(request, f'Your comment has been deleted!')
        return redirect('/book/' + str(bookID))


    context = {
        "comments" : comments,
        "commentContent" : commentContent,
        "commentBook" : commentBook,
        "commentCreatedOn" : commentCreatedOn,
    }
    return render(request, "library_website/delete_Comment.html", context)