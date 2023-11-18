"""

这里是 专门 测试 学习middleware 的

Middleware is a concept commonly used in web frameworks to process requests and responses.
It sits between the web server and the view(就是 view 处理函数), allowing you to modify or process the incoming
 request and outgoing response.




 """

from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin  #这是所有中间件的 父亲

 # 这里按照规范写 一个非常原始的类


#  这是 最原始的 写法， 现在参照 源码的 写法

class MyMD0(object):

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    #进来处理
    print("go in")
    response = self.get_response(request)
    #出去
    print("go out")
    return response



#  这是 参照源码父类 之后的 写法
# 但是还是django 1 里面的 写法： 武沛奇坑人
# The code structure you provided is representative of the older style of defining middleware in Django before Django 1.10. Prior to Django 1.10,
# middleware classes would typically define methods like process_request and process_response to handle requests and responses respectively.
# The newer style of middleware, which you've been working with, is simpler and uses the __call__ method directly.

class MyMD1(object):

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):

    # 请求进来 先走这里
    if hasattr(self, 'process_request'): #看当前类是否有 process_request 这个 method/attribute
      response = self.process_request(request)
      #如果 response 是有值的， 那就不再执行视图函数(使用下面的 or)。什么情况下才能是有值的呢？ 那就是 process_request 这个函数返回了一个值。

    #再走这里， 这里代表执行 view 里面的 视图函数。
    # If the response variable is empty (a falsy value),
    # the code proceeds to the next line and calls self.get_response(request).
    # This is assumed to be the view function that will handle the request and generate a response
    response = response or self.get_response(request);

    if hasattr(self, 'process_response'):
      #这里我直接把上面 辛辛苦苦得到的 response 覆盖掉
      response = self.process_response(request, response)  #这里的 response 是 上面的 response

    return response

  # user 发送一个 request 透过中间件 来的时候， 在进入 view 函数之前
  def process_request(self, request): #因为在上面， 我期望process_request这个函数能够接受一个参数

    #代表意思：  这里是在执行 view之前的， 对 request 进行一下处理
    print("执行 process_request 这个方法")
    request.myAttr = 123 # 比如给 request 加上一个 属性

    return HttpResponse("middleware 已经处理完毕")

  # 用来执行 在 view 函数 处理完之后， request 和 response 发回到 user  也需要 穿过 middleware， 见 day04-中间件 onenote 笔记
  def process_response(self, request, response):
    print("执行 process_response 这个方法")
    return HttpResponse("我谁都不用")





"""
卧槽：武沛奇的教程禁用啊！ 下面的 写法主要是为了升级 Django 1.10 之前版本的中间件 的 方法， Document 里的写法还是 定义 __init__  和  __call__方法

"""

class MyMD(MiddlewareMixin):
  def process_request(self, request):
    print("执行 process_request 这个方法")
    request.myAttr = 123 # 比如给 request 加上一个 属性
    return HttpResponse("middleware 已经处理完毕")

  def process_response(self, request, response):
    print("执行 process_response 这个方法")
    # 一定要有这个， 这个response 就是默认代表 view 函数处理完之后的 response
    # 父亲 MiddlewareMixin 是要求 process_response 这个函数有返回值的。
    return response











