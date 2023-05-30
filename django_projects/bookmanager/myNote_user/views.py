from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User

# Create your views here.


#处理 http://127.0.0.1:8000/user/reg GET请求， 1. 返回 注册页面,  2.处理 注册页面 发回来的 POST 请求
def handle_reg(request):



    #GET, return the register page
    if request.method == "GET":
        return render(request, "myNote_user/01_registPage.html")

    #POST, handle the data  from  "register page", save it into DB

    if request.method == "POST" :
        # get Data from POST
        try:
            username = request.POST.get("username")
            pwd1 = request.POST.get("password1")
            pwd2 = request.POST.get("password2")
        except Exception as e:
            return HttpResponse(e)

        # 2 pwd should be identical
        warn = ""
        if(pwd2 != pwd1):
            warn = "pwd1 and pw2 should be identical"
            return render(request, "myNote_user/01_registPage.html", locals())

        # check if the username already exists
        usernameList = User.objects.filter(username=username)
        if usernameList:
            warn = "the username is taken, please choose another name"
            return render(request, "myNote_user/01_registPage.html", locals())
        # insert pwd(without encrypting the pwd), 你不用插入 拿两个时间戳， 会自动插入
        User.objects.create(username=username, password=pwd1)
        return HttpResponse("register with success")
        pass
