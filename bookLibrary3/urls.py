"""webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from app import views
urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('books/', views.books, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),  # Add this line for editing a book
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('authors/<int:author_id>/edit/', views.edit_author, name='edit_author'),
    path('authors/<int:author_id>/books/', views.author_books, name='author_books'),
    path('publishers/', views.publishers, name='publishers'),
    path('publishers/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),
    path('publishers/<int:publisher_id>/edit/', views.edit_publisher, name='publisher_edit'),
    path('publishers/<int:publisher_id>/authors/', views.publisher_authors, name='publisher_authors'),
    path('booksearch/', views.booksearch, name='booksearch'),
    path('authorsearch/', views.authorsearch, name='authorsearch'),
    path('add-author/', views.add_author, name='add_author'),
    path('add-publisher/', views.add_publisher, name='add_publisher'),
    path('add-book/', views.add_book, name='add_book'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('buy_book/<int:book_id>/', views.buy_book, name='buy_book'),
    path('purchased_books/', views.purchased_books, name='purchased_books'),
    path('remove_purchased_book/<int:book_id>/', views.remove_purchased_book, name='remove_purchased_book'),
]
