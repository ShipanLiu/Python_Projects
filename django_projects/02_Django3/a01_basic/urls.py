from django.urls import path, register_converter, re_path
from . import views
from a01_basic.utils import converters

#自定义类型, 类型名字叫 ”yyyy“
register_converter(converters.MyYearConverter, "yyyy")

urlpatterns = [

    # first request test
    path('t01/', views.t01_handle),

    # http://127.0.0.1:8000/a01/t02_get_login_html/
    path('t02_get_login_html/', views.t02_handle),

    # 动态参数path<>   http://127.0.0.1:8000/a01/t03/2023/jier
    path("t03/<int:year>/<slug:my_slug>/", views.t03_handle),

    #  使用 <str:my_string>  http://127.0.0.1:8000/a01/t04/this%20is%20%20a%20string/
    path("t04/<str:my_string>/", views.t04_string_handle),

    # 使用 <path: my_path>
    path("t05/<path:my_path>/", views.t05_path_handle),


    # 使用 <uuid: my_uuid>
    path("t06/<uuid:my_uuid>/", views.t06_uuid_handle),

    # 使用  自定义类型  http://127.0.0.1:8000/a01/t07/1980/
    path("t07/<yyyy:my_year>/", views.t07_diy_type_handle),


    # use re_path 就相当于 Djando1 中的 url
    # [\w-]  数字， 字母， 下划线,         + 表示 只要有一个 数字
    # http://127.0.0.1:8000/a01/t08/1998/02/jier/
    re_path(r"^t08/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<my_slug>[\w-]+)/$", views.t08_re_path_handle),


    #http://127.0.0.1:8000/a01/t09/page-?
    # http://127.0.0.1:8000/a01/t09/page-100/,  推荐使用 第一种
    re_path(r"^t09/(?:page-(?P<page_number>\d+)/)$", views.t09_handle),
    # re_path(r"^t09/page-(?P<page_number>\d+)/$", views.t09_handle),


    ###########传递默认值#############

    path("t10/", views.handle_t10),
    path("t10/<int:blog_number>", views.handle_t10),

    





]
