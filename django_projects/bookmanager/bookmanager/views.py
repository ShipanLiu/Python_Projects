from django.http import HttpResponse


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


