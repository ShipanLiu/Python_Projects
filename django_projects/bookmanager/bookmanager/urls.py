"""bookmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
#  导入当前 目录下的 views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #http://127.0.0.1:8000
    path('', views.index_view),

    # 不能写成 : views.page1_view(), path() 的 第三个参数是 “page/1” 的别名
    path('page/1', views.page1_view),

    path('page/2', views.page2_view),

    #使用 path 转换器 (除了 1 和 2)
    path('page/<int:pageNr>', views.pages_view),

    # 小计算器 使用re_path, 只接受 1~2 位的 整数
    # (?P<>):  是一个命名分组
    # \d{1, 2} :  一个 1 到 2 位的数
    re_path(r'^(?P<num1>\d{1,2})/(?P<operation>\w+)/(?P<num2>\d{1,2})$', views.calculator2_view),

    # 假如上面的 re_path 不匹配， 那就 用下面的。
    #小计算器： https://127.0.0.1:8000/integer/operation/integer
    path("<int:m>/<str:operation>/<int:n>", views.calculator_view),

    # exercise1:  http://127.0.0.1:8000/birthday/4位数字/1~2位数字/1~2位数字
    re_path(r'^birthday/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$', views.birthday_view),

    # exercise2:  http://127.0.0.1:8000/birthday/1~2位数字/1~2位数字/4位数字
    re_path(r'^birthday/(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{4})$', views.birthday_view),



    ######## 开始 request的探索 ########
    path("test_request", views.test_request),

    path("test_get_post", views.test_get_post),

    # 测试 从templates 文件夹下面 load
    path("test_templates_html", views.test_templates_html),
    # 方式2
    path("test_templates_html2", views.test_templates_html2),




]
