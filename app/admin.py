from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app.models import Author, Publisher, Book

# Register your models here
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)