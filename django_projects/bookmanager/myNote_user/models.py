from django.db import models

# Create your models here.

# User table

class User(models.Model):
    username = models.CharField("username", max_length=30, unique=True)
    password = models.CharField("pwd", max_length=32)
    created_time = models.DateTimeField("create time", auto_now_add=True)
    updated_time = models.DateTimeField("update time", auto_now=True)
    class Meta:
        db_table = 'myNote_user'

    # 自定义 如何显示
    def __str__(self):
        return "username %s"%(self.username)
