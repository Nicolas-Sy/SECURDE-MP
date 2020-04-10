from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='library-home'),
    path('about/', views.about, name='library-about'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='library-book_detail'),
]