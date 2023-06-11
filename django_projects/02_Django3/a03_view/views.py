from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotFound, Http404, JsonResponse, FileResponse
from django.views import View
from django.views.decorators.http import *   # 视图装饰器 @
from django.contrib.auth.decorators import login_required  #必须先登录
from django.shortcuts import render, redirect

# Create your views here.

class t01_CBV_class_base_views(View):
    def get(self, request):
        return HttpResponse("response to GET via CBV class")
    def post(self, request):
        return HttpResponse("response to POST via CBV class")

# 错误页面响应
def t02_handle(request, errorNr):
    if errorNr > 30:
        return HttpResponseNotFound(f"page not found errorNr: {errorNr}")
    # 浏览器 可以识别
    elif errorNr > 20:
        # return HttpResponse(f"page not found errorNr: {errorNr}", status=404)
        raise Http404(f"page not found errorNr: {errorNr}")
    # errorNr <= 20
    else:
        return HttpResponseNotFound(f"page not found errorNr: {errorNr}")


###########视图 装饰器#############
# @require_http_methods(['POST', 'GET'])  #  只允许 POST 和 GET 请求
# @require_GET
@require_POST
def t03_handle(request):
    return HttpResponse("jier")


# 假如你没有登陆， 会自动跳转到  settings.LOGIN_URL
# 或者指定 login url： @login_required(login_url='/polls/login/')
@login_required
def t04_handel(request):
    return HttpResponse("this is the detailed page, login required")

#模仿一下登陆页面， 假如使用了@login_required， 没登陆的话， 会自动登陆到这里
def login_handle(request):
    return HttpResponse("this is login page")

def t05_explore_request_handle(request):
    print(request.scheme) #http
    getQuerySet = request.GET #<QueryDict: {}>
    print(f"request.GET: {getQuerySet}")  #request.GET: <QueryDict: {'a': ['10'], 'b': ['20']}>
    print(f"request.GET： : {list(getQuerySet.items())}") # 访问： http://127.0.0.1:8000/a03/t05/?a=10&b=20  结果#request.GET： : [('a', '10'), ('b', '20')]
    print(request.path) #/a03/t05/
    print(request.method) #GET
    print(request.encoding) #None 表示使用 DEFAULT_CHARSET
    print(request.content_type) #text/plain
    return HttpResponse("success")

# 返回 json 字符串
def t06_json_resonse_handle(request):
    json_value = {
        "name": "jier",
        "pwd": "1234"
    }
    return JsonResponse(json_value)


#返回一个图片
def t07_file_response_handel(request):
    import os
    # getcwd:  E:\Z_Frond_Back_workplace\07_Python\django_projects\02_Django3
    # path = os.getcwd() + "/static/lotos.png"
    # 第二种 合并path的方式
    basePath = os.getcwd()
    newPath = os.path.join(basePath, "static/lotos.png")

    return FileResponse(open(newPath, "rb"))


#urls.py:   app_name = "a03_view"   ,    path("t07/", views.t07_file_response_handel, name="t07_handle_file"),
def t08_redirect_handle(request):
    # 输入 path的 别名
    return redirect("a03_view:t07_handle_file")

# 带着参数的 访问
def t09_redirect_with_parameter_handle(request):
    return redirect("a03_view:t02_errorNr_handle", errorNr=20, permanent=True)  # 302状态码： permanent=True    301状态码： permanent=False



#从一个 table 里面拿到一个 record 或者 404
from django.shortcuts import get_object_or_404
from a03_view.models import Question
def t10_get_object_or_404_handle(request, ques_id):
    question = get_object_or_404(Question, pk=ques_id)
    # locals() 会自动把 多有的 local 变量 装进 dict， 然后传到 htmlpage 里面
    return render(request, "a03_view/01_from_model_to_html.html", locals())

#假如成功的话
# Q1
# this is my first question


#假如出错的话
# Page not found (404)
    # No Question matches the given query.
        # Request Method:	GET
            # Request URL:	http://127.0.0.1:8000/a03/t10/1
                # Raised by:	a03_view.views.t10_get_object_or_404_handle


# line11  发现继承的是 View， 可不可以继承 其他的 View呢？
# 参数 pk 不用传入， dj 会自动处理。
from django.views import generic
class T11DetailedVieww(generic.DetailView): # 不再继承View， 而是继承 DetailView
    model = Question
    template_name = "a03_view/02_from_model_to_html.html"








