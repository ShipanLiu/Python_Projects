from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # first request test
    path('t01/', views.t01_handle),

    # http://127.0.0.1:8000/a01/t02_get_login_html/
    path('t02_get_login_html/', views.t02_handle),


]
