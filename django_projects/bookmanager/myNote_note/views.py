from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.

def handle_notes(request):
    uid = -1
    if request.method == "GET":
        # 判断是否登陆，看session 是否过期了
        if request.session.get("username") and request.session.get("uid"):
            uid = request.session.get("uid")
            print("session ok")
            # 如果登陆， 查出当前用户的 notes
            notes = Note.objects.filter(user_id=uid)
            return render(request, "myNote_note/01_list_note.html", locals())

        # 这里假如session 过期， 那么就使用 cookie
        cookie_username = request.COOKIES.get("username")
        cookie_uid = request.COOKIES.get("uid")

        if cookie_username and cookie_uid:
            uid = cookie_uid
            print("session bad")
            print("cookie ok")
            # refresh session
            request.session["username"] = cookie_username
            request.session["uid"] = cookie_uid
            notes = Note.objects.filter(user_id=uid)
            return render(request, "myNote_note/01_list_note.html", locals())

        # 我现在就是没有登陆
        return render(request, "myNote_user/02_loginPage.html")

def handle_view_content(request):
    pass


def handle_add(request):
    pass


def handle_delete(request):
    pass



def handle_update(request):
    pass
