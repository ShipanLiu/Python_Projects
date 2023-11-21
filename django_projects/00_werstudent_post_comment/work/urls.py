from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.work_handle),
    path("picker1", views.picker_handle),
    path("picker2", views.picker_handle2),
]
