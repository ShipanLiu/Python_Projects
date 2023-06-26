from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "myNote_note"


urlpatterns = [

    path("", views.handle_notes, name="handle_notes"),

]
