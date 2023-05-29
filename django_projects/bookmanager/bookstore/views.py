from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book

def all_books(request):

    # is_active=True  表示没有被删除的
    books = Book.objects.filter(is_active=True);
    #go to the html file and bring some data

    dict = {
        "books": books
    }

    # 使用 locals()
    # return render(request, "bookstore/01_all_book.html", locals())

    # 使用自己封装的 方式
    return render(request, "bookstore/01_all_book.html", dict)


def update_book(request, book_id):
    # get this Book by using id, the id is in path
    try:
        # 只对 未删除的数据 更新
        book = Book.objects.get(id=book_id, is_active=True)
    except Exception as e:
        print("--update book error: %s"%e)
        return HttpResponse("--book does not exist")

    # 这里不是 发 request 的， 而是 处理发来  的request 的。
    if request.method == "GET":
        return render(request, "bookstore/02_update_book.html", locals())

    elif request.method == "POST":

        # 把 值 提取出来
        price = request.POST["price"]
        print("price: ", price)
        market_price = request.POST["market_price"]
        info = request.POST["info"]

        # update
        book.price = price
        book.market_price = market_price
        book.info = info
        # save
        book.save()

        # 保存之后 302内部跳转, 这里 写相对地址
        return HttpResponseRedirect("/bookstore/all_books")

def delete_book(request):

    # 和 update_book 不一样， 我们 通过 提取 url GET方式的   /delete_book?book_id=1 里面的 book_id
    # get book_id from url and query
    book_id = request.GET.get("book_id")
    # 假如 bookid 没有给
    if not book_id:
        return HttpResponse("--book_id wrong--")

    try:
        book = Book.objects.get(id=book_id, is_active=True)
    except Exception as e:
        return HttpResponse(e)
    # set is_active = False
    book.is_active = False

    # save
    book.save()

    # 302 redirect to all_books (写绝对路径)
    return HttpResponseRedirect("/bookstore/all_books")




