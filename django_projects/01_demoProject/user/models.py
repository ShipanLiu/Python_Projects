from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField("username", max_length=30, unique=True)
    password = models.CharField("pwd", max_length=32) # md5 加密是 32个hex
    created_time = models.DateTimeField("create time", auto_now_add=True)
    updated_time = models.DateTimeField("update time", auto_now=True)
    class Meta:
        db_table = 'demo_user'

    def __str__(self):
        return "username %s"%(self.username)
