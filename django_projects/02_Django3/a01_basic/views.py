from django.http import HttpResponse
from django.shortcuts import render

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
