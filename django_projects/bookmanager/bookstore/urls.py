from django.urls import path
from . import views


urlpatterns = [

    # http;//127.0.0.1:8000/bookstore/all_books
    path("all_books", views.all_books, name="all_books"),


    # 01_all_book.html  和  02_update_book.html 里面的 http 请求
    # update_book/<int:book_id> 里面的 book_id 会 自动传给 views.update_book() 函数
    path("update_book/<int:book_id>", views.update_book, name="update_book"),

    # delete  book
   path("delete_book", views.delete_book, name="delete_book")

]
