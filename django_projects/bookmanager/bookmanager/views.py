from django.http import HttpResponse, HttpResponseRedirect
# html从 templeates 文件夹 拿出来方式1
from django.template import loader
# html从 templeates 文件夹 拿出来方式2
from django.shortcuts import render


POST_FORM = """
    <form method="post" action="/test_get_post">
        username: <input type="text" name="uname"/>
        <input type="submit" value="submit"/>
    </form>
"""


def index_view(request):
    html = "<h1>index view</h1>"
    # HttpResponse  就接受一个 string
    return HttpResponse(html)
def page1_view(request):
    html = "<h1>this is my first page</h1>"
    # HttpResponse  就接受一个 string
    return HttpResponse(html)
def page2_view(request):
    html = "<h1>this is my second page</h1>"
    # HttpResponse  就接受一个 string
    return HttpResponse(html)

#使用 path 转换器
# pageNr 和  path('page/<int:pageNr>', views.pages_view) 里的pageNr 名字要一致
def pages_view(request, pageNr):
    # %s  也可以接受 int 类型
    str = "this is page %s"%(pageNr)
    return HttpResponse(str)

#计算器项目
def calculator_view(request, m, operation, n):
    if operation not in ["add", "sub", "mul"]:
        return  HttpResponse("wrong operation")

    result = 0
    if operation == "add":
        result =  m + n
    elif operation == "sub":
        result = m - n
    elif operation == "mul":
        result = m * n

    return HttpResponse("the result: %s"%(result))

def calculator2_view(request, num1, operation, num2):
    html = "num1: %s, operation: %s, num2: %s"%(num1, operation, num2)
    return HttpResponse(html)

def birthday_view(request, year, month, day):
    str = "生日是: %s年%s月%s日"%(year, month, day)
    return HttpResponse(str);



#   day 02 :  开始  rquest 了

def test_request(request):

    print("path info is: ", request.path_info) #path info is:  /test_request
    print("method is: ", request.method) #method is:  GET
    print("query dict is: ", request.GET) #http://localhost:8000/test_request?uid=0&pwd=1  ===> <QueryDict: {'uid': ['0'], 'pwd': ['1']}>
                                            # 注意 value 是  array
    print("full path is: ", request.get_full_path())   #full path is:  /test_request?uid=0&pwd=1
    print("META is: ", request.META)  # META["REMOTE_ADDR"] 是客户端ip 地址
    # return HttpResponse("test request ok!")
    # 重定向 到page1
    return HttpResponseRedirect("/page/1")


# GET and POST
def test_get_post(request):
    if request.method == "GET":

        #http://localhost:8000/test_get_post?a=400&c=600
        # print(request.GET['a']) # 很暴力， 假如 url 里没有 ’a‘ 的话， 那么会有 “MultiValueDictKeyError” 错误
        # with default value
        print(request.GET.get('c', "c does not exist"))
        return HttpResponse(POST_FORM)
    elif request.method == "POST":
        #form 的 post 请求 给了我 一个 request 和 form 的 data
        uname = request.POST.get("uname", "unknown value")
        print("uname is: ", uname)
        return HttpResponse("form data - uname: " + uname)
    else:
        pass
    return HttpResponse("test get post ok!")



#开始 Templates 的 书写
def test_templates_html(request):
    # load html file, this will find the html under bookmanager/tempaltes automaticially
    t = loader.get_template("01_testHtmlTemplate.html")
    # convert html file to string
    htmlStr = t.render()
    return HttpResponse(htmlStr)

# 更简单的 模板加载方法
def test_templates_html2(request):

    # 模拟 View 层 给的 值
    dic = {
        "username": "jier",
        "age": 25
    }

    # 找到 html + 值 传进去
    return render(request, "01_testHtmlTemplate.html", dic)






