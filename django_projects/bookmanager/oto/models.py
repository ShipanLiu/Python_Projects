from django.db import models

#  演示  one to one 的 外键 关系映射

# Create your models here.
class Author(models.Model):
    name = models.CharField("author_name", max_length=10)

class wife(models.Model):
    name = models.CharField("wife name", max_length=10)
    # 创建 FK， 关联一张表
    husband = models.OneToOneField(Author, on_delete=models.CASCADE)
