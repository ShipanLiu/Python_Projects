from django.urls import path, include
from a03_view import views

app_name = "a03_view"

# 不用纠结进入father path， 引入app 就直接 import
import a01_basic

urlpatterns = [
    #  使用 class based view 进行 request 的 回复
    path("t01/", views.t01_CBV_class_base_views.as_view()),

    # 错误处理
    path("t02/<int:errorNr>", views.t02_handle, name="t02_errorNr_handle"),

    # 视图 装饰器， decorator
    path("t03/", views.t03_handle),

    #要求用户登陆 才能访问 t04
    path("t04/", views.t04_handel),

    #配置一下 登陆页面：
    path("login/", views.login_handle),

    #探讨 request 俩民到底有什么
    path("t05/", views.t05_explore_request_handle),


    #JsonResponse
    path("t06/", views.t06_json_resonse_handle),


    #FileResponse  ==>  发送一个 img
    path("t07/", views.t07_file_response_handel, name="t07_handle_file"),


    # 测试 redirect ==》 redirect 到另外一个 view function
    path("t08/", views.t08_redirect_handle),

    # 测试 redirect ==》 redirect 到另外一个 view function， 带参数
    path("t09/", views.t09_redirect_with_parameter_handle),



    #从一个 table 里面拿到一个 record 或者 404
    path("t10/<int:ques_id>", views.t10_get_object_or_404_handle)


    # from django.views import generic 里面  除了 View 意外， 还有 DetailView， ListView。。。。






]
