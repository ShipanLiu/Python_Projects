from django.urls import path
from . import views


urlpatterns = [

    # http;//127.0.0.1:8000/bookstore/all_books
    path("all_books", views.all_books, name="all_books")

]
