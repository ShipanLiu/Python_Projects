from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
import uuid


# Create your views here.

# handle my first request
def t01_handle(reuqest):
    return HttpResponse("success")


def t02_handle(request):
    # ['COOKIES', 'FILES', 'GET', 'META', 'POST', '__class__', '__delattr__', '__dict__',
    # '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
    # '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__',
    # '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
    # '__str__', '__subclasshook__', '__weakref__', '_current_scheme_host', '_encoding', '_get_full_path',
    # '_get_post', '_get_raw_host', '_get_scheme', '_initialize_handlers', '_load_post_and_files',
    # '_mark_post_parse_error', '_messages', '_read_started', '_set_content_type_params', '_set_post',
    # '_stream', '_upload_handlers', 'accepted_types', 'accepts', 'body', 'build_absolute_uri', 'close',
    # 'content_params', 'content_type', 'csrf_processing_done', 'encoding', 'environ', 'get_full_path',
    # 'get_full_path_info', 'get_host', 'get_port', 'get_raw_uri', 'get_signed_cookie', 'headers', 'is_ajax',
    # 'is_secure', 'method', 'parse_file_upload', 'path', 'path_info', 'read', 'readline', 'readlines',
    # 'resolver_match', 'scheme', 'session', 'upload_handlers', 'user']
    print(dir(request))
    return render(request, "a01_basic/01_test_html.html")


# 动态path 带参数
def t03_handle(request, year, my_slug):
    # 等价于： "the year is: %s"%{year}
    # 这是 f-string，
    return HttpResponse(f"the year and slug are : {year}, slug: {my_slug}")


def t04_string_handle(request, my_string):
    return HttpResponse(f"my_string: {my_string}")


#  http://127.0.0.1:8000/a01/t05/jier/01/   ====>  my_path: jier/01
def t05_path_handle(request, my_path):
    return HttpResponse(f"my_path: {my_path}")


#  http://127.0.0.1:8000/a01/t06/ab621f25-052d-11ee-9af7-54e1ad7927b0/  ===>  my_uuid: ab621f25-052d-11ee-9af7-54e1ad7927b0
print(uuid.uuid1())  # 17ebea7d-052d-11ee-bf20-54e1ad7927b0


def t06_uuid_handle(request, my_uuid):
    return HttpResponse(f"my_uuid: {my_uuid}")


# http://127.0.0.1:8000/a01/t07/1980/  ==> my_year: 1980
def t07_diy_type_handle(request, my_year):
    return HttpResponse(f"my_year: {my_year}")


def t08_re_path_handle(request, year, month, my_slug):
    return HttpResponse(f"year: {year}, month: {month}, my_slug: {my_slug}")


def t09_handle(request, page_number):
    return HttpResponse(f"page_number: {page_number}")


# 假如没有传 blog_number，blog_number  默认值是 2
#  http://127.0.0.1:8000/a01/t10/  ===》 blog_number: 2
#  http://127.0.0.1:8000/a01/t10/999  ==》 blog_number: 999
def handle_t10(request, blog_number=2):
    return HttpResponse(f"blog_number: {blog_number}")


def t11_handle_history(request):
    return HttpResponse("history")


def t11_handle_edit(request):
    return HttpResponse("edit")


def t11_handle_discuss(request):
    return HttpResponse("discuss")


# http://127.0.0.1:8000/a01/t12/  ===>  username: jier, pwd: 1234
def t12_handle(request, username, pwd):
    return HttpResponse(f"username: {username}, pwd: {pwd}")


# 测试 反向解析
# http://127.0.0.1:8000/a01/t13   ===>   http://127.0.0.1:8000/a01/t14/1998/
def t13_handle(request):
    # goto path("t14/<int:number>", views.t14_handle, name="t14_path")
    # 第一种方法 redirect， 带参数
    # http://127.0.0.1:8000/a01/t13   ===>   http://127.0.0.1:8000/a01/t14/1998/
    # return HttpResponseRedirect("/a01/t14/1998/")

    # 第一种方法 redirect， 带参数
    # 我要忘记 传参数， reverse 里用的是 ”t14“, 用于 url 反向解析
    # a01_basic:t14_path ==> a01_basic 是 urls.py 里面的 app_name = "a01_basic"， t14_path 是 path name
    # http://127.0.0.1:8000/a01/t13 ===> http://127.0.0.1:8000/a01/t14/2023/
    # return HttpResponseRedirect(reverse("a01_basic:t14_path", args=[2023]))

    # 我直接跳到html， 在 html 中 访问 "t14"
    return render(request, "a01_basic/02_jumpt_to_another_view_function.html")


def t14_handle(request, number=999):  # num 默认值 999
    # 访问 其他 path
    return HttpResponse(f"welcome to t14, num: {number}")
