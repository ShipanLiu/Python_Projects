from django.shortcuts import render
from .models import Book

def all_books(request):
    books = Book.objects.all();
    #go to the html file and bring some data
    return render(request, "bookstore/01_all_book.html", locals())

