from django.contrib import admin
from django.urls import path, re_path, include
from . import views


urlpatterns = [

    # for registpage
    #myNote/user/reg
    path("reg", views.handle_reg, name="reg"),
    path("login", views.handle_login, name="login"),
    path("logout", views.handle_logout, name="logout")
]
