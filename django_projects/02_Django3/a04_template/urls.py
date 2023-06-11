from django.urls import path
from a04_template import views

urlpatterns = [

    #  模板引擎
    path("t01/<int:pk>", views.t01_template_engine_handle1),
]
