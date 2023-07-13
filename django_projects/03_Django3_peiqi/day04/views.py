from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def t01_handle(request):
    print(request.myAttr) #这里是 middleware 里面给 request 加的一个 自定义属性
    return HttpResponse(f"the attribute of request that is added by middleware is: {request.myAttr}")
