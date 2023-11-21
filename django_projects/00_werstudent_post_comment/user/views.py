from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import hashlib


# Create your views here.

def handle_reg(request):
    # GET, return the register page
    if request.method == "GET":
        return render(request, "user/userRegistPage.html")

    # POST, handle the data  from  "register page", save it into DB

    if request.method == "POST":
        # get Data from POST
        username = request.POST.get("username")
        pwd1 = request.POST.get("password1")
        pwd2 = request.POST.get("password2")

        # 2 pwd should be identical
        warn = ""
        if ( not username)  or (not pwd1) or (not pwd2):
            warn = "input can't be empty"
            return render(request, "user/userRegistPage.html", locals())  # 让form显示old提交数据
        if (pwd2 != pwd1):
            warn = "pwd1 and pw2 should be identical"
            return render(request, "user/userRegistPage.html", locals())  # 让form显示old提交数据
        else:
            m = hashlib.md5()  # create a md5 object
            m.update(pwd1.encode())
            pwd_md5 = m.hexdigest()
            pass

        # check if the username already exists
        usernameList = User.objects.filter(username=username)
        if usernameList:
            warn = "the username is taken, please choose another name"
            return render(request, "user/userRegistPage.html", locals())

        try:
            user = User.objects.create(username=username, password=pwd_md5)
        except Exception as e:
            print("create user error: %s" % (e))
            warn = "the username is taken, please choose another name"
            return render(request, "user/userRegistPage.html", locals())

        # 免登 session
        request.session["username"] = username
        request.session["uid"] = user.id

        return HttpResponseRedirect("/index")


# http://127.0.0.1:8000/myNote/user  /login
def handle_login(request):
    # receive GET request ==> return login page
    if request.method == "GET":

        if request.session.get("username") and request.session.get("uid"):
            print("session ok")
            return HttpResponseRedirect("/index")

        return render(request, "user/userLoginPage.html")

    # receive POST request ==> login
    elif request.method == "POST":
        # first get data
        warn = ""
        username = request.POST.get("username")
        password = request.POST.get("password")

        # check
        if (not username) or (not password):
            warn = "input area can'be be empty"
            return render(request, "user/userLoginPage.html", locals())

        # get user from DB
        try:
            userFound = User.objects.get(username=username)
        except Exception as e:
            print("--login user error %s" % (e))
            warn = "user name does not exist in DB"
            # reset input
            dict = locals()
            dict["username"] = ""
            dict["password"] = ""
            return render(request, "myNote_user/userLoginPage.html", dict)

        # md5 the inputed password
        m = hashlib.md5()
        m.update(password.encode())
        # compare with pwd from DB，
        if m.hexdigest() != userFound.password:
            warn = "user name exists but pwd is wrong"
            dict = locals()
            dict["password"] = ""
            return render(request, "user/userLoginPage.html", dict)

        request.session["username"] = username
        request.session["uid"] = userFound.id

        response = HttpResponseRedirect("/index")

        return response


def handle_logout(request):
    # check if cookies and sessions exist or not
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('/index')
    return resp

