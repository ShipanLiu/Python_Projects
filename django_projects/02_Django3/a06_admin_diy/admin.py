from django.contrib import admin
from django.db.models import F

# Register your models here.  使用系统默认方式： admin.site.register(table_name)

# 现在使用 自定义的 管理类
from .models import *


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 自定义管理模型
class PersonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "age"]  #这是按照attribute 来依次；  ID     PEROSON_NAME     PERSON_AGE

    # age 降序 30 25
    ordering = ['-age']

# 1.para: table name  2.para: 自定义管理类
admin.site.register(Person, PersonAdmin)



#<<<<<<<<<<<<<<<<<<<使用装饰器<<<<<<<<<<<<<<<<<<<<<<<

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "age"]
    ordering = ['-age']
    empty_value_display = 'null'  # 当可以是 null的时候 name = models.CharField("worker_name", max_length=20, null=True, blank=True)
    fields = ('age',)  #if you add a new worker, you can only input the age, the name is gone

    #  自定义批量处理函数
    def age_add_one(table, request, queryset):
        queryset.update(age=F('age') + 1)

    # 操作的描述
    age_add_one.short_description = "all worker age+1"

    # 自定义批量操作, 给每个工人 加一岁
    actions = [age_add_one]

