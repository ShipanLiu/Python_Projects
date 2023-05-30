from django.contrib import admin
from django.urls import path, re_path, include
from . import views


urlpatterns = [

    # for registpage
    path("reg", views.handle_reg, name="reg")
]
