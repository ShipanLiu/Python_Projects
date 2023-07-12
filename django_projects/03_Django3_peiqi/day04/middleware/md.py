"""

这里是 专门 测试 学习middleware 的

Middleware is a concept commonly used in web frameworks to process requests and responses.
It sits between the web server and the view(就是 view 处理函数), allowing you to modify or process the incoming
 request and outgoing response.




 """

 # 这里按照规范写 一个非常原始的类



class MyMD(object):

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    #进来处理
    print("go in")
    response = self.get_response(request)
    #出去
    print("go out")
    return response
