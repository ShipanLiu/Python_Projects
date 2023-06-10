from django.urls import path, include
from a03_view import views

# 不用纠结进入father path， 引入app 就直接 import
import a01_basic

urlpatterns = [
    #  使用 class based view 进行 request 的 回复
    path("t01/", views.t01_CBV_class_base_views.as_view()),

    # 错误处理
    path("t02/<int:errorNr>", views.t02_handle)


]
