#  visit :  http://127.0.0.1:8000/admin

from django.contrib import admin
from .models import Book
from .models import Author



# 自定义 admin 后台的 管理页面, 继承 admin.ModelAdmin
class BookManager(admin.ModelAdmin):
    # 显示 table 里的 那些字段
    list_display = ["id", "title", "pub", "info", "price", "market_price", "is_active"]

    #哪个显示成超链接 的蓝色方式
    list_display_links = ["title"]

    #add filter
    list_filter = ["pub"]

    # add search field, 搜索依据， 模糊查询
    search_fields = ["title", "pub"]

    #在列表上直接修改, 和 list_display_links 互斥
    list_editable = ["price", "info"]


class AuthorManager(admin.ModelAdmin):

    list_display = ["id", "name", "age", "email"]








# Register your models here.
admin.site.register(Book, BookManager)
admin.site.register(Author,AuthorManager)





