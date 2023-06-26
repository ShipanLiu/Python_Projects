from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "myNote_user"


urlpatterns = [

    # for registpage
    #myNote/user/reg
    path("reg", views.handle_reg, name="reg"), # this is for register
    path("login", views.handle_login, name="login"),
    path("logout", views.handle_logout, name="logout")
]
