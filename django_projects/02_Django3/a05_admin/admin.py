from django.contrib import admin
from .models import *
# Register your models here.
# 要想你的应用在这里展现： 那就需要
admin.site.register(Student)

# 每次新创建 一个 table， 就要在 这里加上
admin.site.register(Place)
admin.site.register(Restaurant)
admin.site.register(Waiter)

# 多对多
admin.site.register(SchoolClass)
admin.site.register(Teacher)
