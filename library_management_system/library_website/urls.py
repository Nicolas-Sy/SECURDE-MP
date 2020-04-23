from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='library-home'),
    path('about/', views.about, name='library-about'),
    # path('book/<int:pk>', views.BookDetailView.as_view(), name='library-book_detail'),
    path('createBook/', views.createBook, name='library-create_book'),
    path('editBook/<int:pk>/', views.updateBook, name='library-update_book'),
    path('deleteBook/<int:pk>/', views.deleteBook, name='library-delete_book'),
    path('createBookInstance/', views.createBookInstance, name='library-create_bookInstance'),
    path('editBookInstance/<uuid:pk>', views.updateBookInstance, name='library-update_bookInstance'),
    path('deleteBookInstance/<uuid:pk>', views.deleteBookInstance, name='library-delete_bookInstance'),
    path('book/<int:pk>', views.bookDetail, name='library-book_detail'),
    path('borrowBook/<uuid:pk>', views.borrowBookInstance, name ='library-borrow_book'),
    path('returnBook/<uuid:pk>', views.returnBookInstance, name ='library-return_book'),
    path('editComment/<uuid:pk>', views.editComment, name ='library-edit_comment'),
    path('deleteComment/<uuid:pk>', views.deleteComment, name ='library-delete_comment'),
]