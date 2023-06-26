from django.db import models
from myNote_user.models import User

# Create your models here.
# 创建笔记类
class Note(models.Model):
    title = models.CharField("title", max_length=100)
    content = models.TextField("content")
    create_time = models.DateTimeField("create_time", auto_now_add=True)
    update_time = models.DateTimeField("update_time", auto_now=True)
    # 每一个笔记都有一个user, 每个user 可以有多个 notes， 典型一对多， 那么在多的一方 添加外键
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.pk}--{self.title}--{self.user.username}"

    class Meta:
        db_table = "myNote_note"
