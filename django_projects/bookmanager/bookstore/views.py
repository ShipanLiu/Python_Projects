from django.shortcuts import render
from .models import Book

def all_books(request):
    books = Book.objects.all();
    #go to the html file and bring some data

    dict = {
        "books": books
    }

    # 使用 locals()
    # return render(request, "bookstore/01_all_book.html", locals())

    # 使用自己封装的 方式
    return render(request, "bookstore/01_all_book.html", dict)

